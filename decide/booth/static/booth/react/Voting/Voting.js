"use strict";

const { useState, useEffect } = React;

let firstRender = true;
let votingType = null;
let alumList = null;



const Voting = ({ utils }) => {
  /*#################################################################*/
  /*####################### UTILITY FUNCTIONS #######################*/
  /*#################################################################*/

  const dictionary = {
    Man: "1",
    Woman: "2",
    Other: "3",
    Software: "1",
    "Computer Technology": "2",
    "Information Technology": "3",
    Health: "4",
    First: "1",
    Second: "2",
    Third: "3",
    Fourth: "4",
    Master: "5",
  };

  const getVotingType = () => {
    let res = "";
    if (voting.tipo === "PV") res = "primary";
    else if (voting.tipo === "GV") res = "general";
    else {
      res = "error";
      utils.setAlert({
        lvl: "error",
        msg: utils.lang["internalError"],
      });
    }

    return res;
  };

  const bigpk = {
    p: BigInt.fromJSONObject(voting.pub_key.p.toString()),
    g: BigInt.fromJSONObject(voting.pub_key.g.toString()),
    y: BigInt.fromJSONObject(voting.pub_key.y.toString()),
  };

  const encrypt = (options) => {
    const bigmsg = BigInt.fromJSONObject(options);
    const cipher = ElGamal.encrypt(bigpk, bigmsg);
    return { a: cipher.alpha.toString(), b: cipher.beta.toString() };
  };

  const encryptAll = (options) => {
    for (let o in options) {

      if (Array.isArray(options[o])) {
        for (let p in options[o]) {
          options[o][p] = encrypt(options[o][p].toString());
        }
      } else if (dictionary[options[o]]) {
        options[o] = encrypt(dictionary[options[o]]);
      } else {
        options[o] = encrypt(options[o].toString());
      }
    }
    console.log(options);
    return options;
  };

  const getGenresByIds = async (ids) => {
    let res = null;

    await utils
      .post("/authentication/decide/getGenresByIds/", ids)
      .then((result) => {
        res = result;
      })
      .catch((error) => {
        utils.setAlert({
          lvl: "error",
          msg: utils.lang["internalError"],
        });
      });

    return res.genres;
  };

  const checkRestrictions = async (ids) => {
    let res = true;

    let genres = await getGenresByIds(ids);
    let males = 0;
    let females = 0;
    let others = 0;

    for (let i = 0; i < genres.length; i++) {
      if (genres[i] === "Man") males = males + 1;
      else if (genres[i] === "Woman") females = females + 1;
      else others = others + 1;
    }

    if (males > 5 || females > 5 || males + females + others > 10) res = false;

    return res;
  };

  const getInput = async () => {
    let res = {};

    let questions = document.getElementsByClassName("question");

    let cont1 = 0
    for (let i = 0; i < questions.length; i++) {
      const titulo = questions[i].children[0].innerHTML.replace(' <h2 style="text-transform: uppercase;"><strong>', "").replace("</strong></h2>", "").replace("<h2>", "").replace("</h2>", "");
      let inputs = questions[i].getElementsByTagName("input");
      for (let j = 0; j < inputs.length; j++) {
        if (inputs[j].checked) {
          res[titulo] = inputs[j].value;

          cont1 = cont1 + 1
        }
      }
    }
    res["sex"] = utils.votingUserData.sex;
    res["age"] = utils.votingUserData.age;
    res["grade"] = utils.votingUserData.grade;
    res["year"] = utils.votingUserData.year;

    if (votingType === "general") {
      let la = document.getElementsByClassName("alum-list");
      let alumnsId = [];
      let alumnsNumber = [];
      let inputs = la[0].getElementsByTagName("input");
      let cont2 = 0

      for (let j = 0; j < inputs.length; j++) {
        if (inputs[j].checked) {
          alumnsId.push(inputs[j].value.split(" ")[0]);
          alumnsNumber.push(inputs[j].value.split(" ")[1])
          cont2 = cont2 + 1
        }
      }
      res[la[0].children[0].innerHTML.replace("<h2>", "").replace("</h2>", "")] = alumnsNumber;

      const valid = await checkRestrictions(alumnsId);
      cont1 = cont1 - cont2;
      if (!valid || cont1 < 2 || cont2 === 0) res = false;

    } else {
      if (cont1 < 2) res = false;
    }
    console.log(res)
    return res;
  };

  const closeAlert = () => {
    if (utils.alert.lvl === "errorGeneral" || utils.alert.lvl === "errorPrimary" || utils.alert.lvl === "error" ) {
      utils.setAlert({ lvl: null, msg: null });
      location.reload()
    } else {
      utils.setAlert({ lvl: null, msg: null });
      location.replace("/booth")
    }
  };

  const Modals = () => {
    const [isOpen, setIsOpen] = useState(false);

    const showModal = () => {
      setIsOpen(true);
    };

    const hideModal = () => {
      setIsOpen(false);
    };

    return (
      <div>
        {/* Aqui empieza */}
        <button
          type="button"
          className="btn btn-outline-dark"
          data-toggle="modal"
          data-target="#exampleModal"
        >
          {utils.lang["modal_button"]}

          {/* Bases de la votación */}
        </button>

        <div
          className="modal fade"
          id="exampleModal"
          tabIndex="-1"
          role="dialog"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="exampleModalLabel">
                  {utils.lang["modal_title"]}
                </h5>
                <button
                  type="button"
                  className="close"
                  data-dismiss="modal"
                  aria-label="Close"
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div className="modal-body">
                {utils.lang["modal_body"]}

              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-dismiss="modal">
                  {utils.lang["modal_close_button"]}
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    );
  };

  const sendVoting = async (event) => {
    event.preventDefault();

    const options = await getInput();

    if (options) {

      const v = encryptAll(options);

      setSendVotingAnimation(true);
      setTimeout(() => {
        setSendVotingAnimation(false);
      }, 3000);

      const data = {
        vote: v,
        voting: voting.id,
        voter: utils.votingUserData.user_id,
        token: utils.votingUserData.token,
      };
      utils
        .post("/gateway/store/", data)
        .then((data) => {
          setTimeout(() => {
            utils.setAlert({
              lvl: "success",
              msg: utils.lang["congratulations"],
            });
          }, 1700);
        })
        .catch((error) => {
          utils.setAlert({ lvl: "error", msg: "Error: " + error });
        });

    } else {
      if (votingType === "general") {
        utils.setAlert({
          lvl: "errorGeneral",
          msg: utils.lang["bigError"],
        });
      } else {
        utils.setAlert({
          lvl: "errorPrimary",
          msg: utils.lang["blankError"],
        });
      }
    }
  };

  const filterQuestions = () => {
    let res = [];
    let year = dictionary[utils.votingUserData.year];
    year = year - 1;
    const q1 = voting.question[year];
    const q2 = voting.question[5];
    res.push(q1);
    res.push(q2);

    if (votingType === "general") {
      const q3 = voting.question[6];
      res.push(q3);
    }
    voting.question = res;

    return res;
  };

  /*#####################################################*/
  /*####################### STATE #######################*/
  /*#####################################################*/
  const [sendVotingAnimation, setSendVotingAnimation] = useState(false);

  /*#############################################*/
  /*############### FUNCTIONALITY ###############*/
  /*#############################################*/

  if (firstRender) {
    votingType = getVotingType();
    filterQuestions();
    if (votingType === "general") {
      alumList = voting.question[2];
    }
  }

  useEffect(() => {
    firstRender = false;
    $(document).ready(function () {

      $("div.question:first-of-type").addClass("active-question")

      $("button#prev-question").css({
        display: "none",
      });

      var colors = new Array(
        "#426A7A",
        "#439192",
        "#E4A282"
      );
     
      $(".question").each(function (index) {

        $(this).css({
          "background-color": colors[index],
          filter: "brightness(90%)",
        });
        $(this).find(".flip-card-back").css({
          "background-color": colors[index],
        });
      });

      $("button#next-question").click(function () {
        var active_question = $("div.active-question");
        updateButtons(active_question.next());

        if (active_question.next().hasClass("question")) {
          active_question.removeClass("active-question");
          active_question.next().addClass("active-question");

        }
      });
      $("button#prev-question").click(function () {

        var active_question = $("div.active-question");
        updateButtons(active_question.prev());

        if (active_question.prev().hasClass("question")) {
          active_question.removeClass("active-question");
          active_question.prev().addClass("active-question");

        }
      });

      $("input").on("click", function () {

        var this_card = $(this).parent().parent().parent();

        var this_question = this_card.parent().parent().parent().parent().parent();

        if (this_card.hasClass("flipped")) {
          this_card.removeClass("flipped");
          $(this).prop('checked', false);

        } else {
          var flipped_card = $(this_question).find("div.flip-card.flipped")
          flipped_card.removeClass("flipped");
          flipped_card.prop('checked', false);

          this_card.addClass("flipped");
        }

      });

    });
  }, []);

  // COSAS DEL ESTILO
  function updateButtons(question_to_update) {
    // Si existe una pregunta posterior
    if (question_to_update.next().hasClass("question")) {
      $("button#next-question").css({
        display: "block",
      });
    } else {
      $("button#next-question").css({
        display: "none",
      });
    }
    if (question_to_update.prev().hasClass("question")) {
      $("button#prev-question").css({
        display: "block",
      });
    } else {
      $("button#prev-question").css({
        display: "none",
      });
    }
  }

  //   show the first element, the others are hide by default

  /*############### RETURN ###############*/
  return (
    <div id="voting-body" className="voting container-fluid">

      <div className="row justify-content-between align-items-center">
        <div className="col-3">
          <button id="prev-question" type="button" className="btn btn-outline-dark">
            {utils.lang["prev"]}
          </button>{" "}
        </div>
        <div >
          <div className="moda">{<Modals />}</div>
        <div className="but">
          <button className="languageButton" onClick={utils.changeLanguage}><img className="languageImg" src={utils.lang["language_button"]} /></button>
          </div>
        </div>
        <div className="col-3">
          {" "}
          <button
            id="next-question"
            type="button"
            className="btn btn-outline-dark"
          >
            {utils.lang["next"]}

          </button>
        </div>
      </div>
      <div className="row">
        <div className="col">
          <form onSubmit={sendVoting}>

            {voting.question.slice(0, 2).map((o) => (
              <div className="question" key={o.desc}>
                <div align="center">
                  {" "}
                  <h2 style={{textTransform: 'uppercase'}}><strong>{o.desc}</strong></h2>
                </div>
                <div className="container-fluid ">
                  <div className="boxesDiv">
                    {sendVotingAnimation && (
                      <div className="votingAnimation">
                        <a id="rotator">
                          <img src="https://image.flaticon.com/icons/png/512/91/91848.png" />
                        </a>
                      </div>
                    )}
                    {o.options.map((p) => (
                      <div key={p.number}>
                        <div className="option p-3">
                          <div className="card-input">
                            <label>
                              <div className="flip-card">
                                <div className="flip-card-inner">
                                  <div className="flip-card-front">
                                    <input
                                      type="radio"
                                      name={o.desc}
                                      className="card-input-element"
                                      value={p.number}
                                    />

                                    <h4>{utils.lang["cand"]}</h4><br/>
                                    <h3>{p.option.split(" / ")[0]}</h3>
                                    <img className="responsive" src="https://www.uco.es/investigacion/proyectos/SEBASENet/images/Logo_US.png" alt="logo"></img>
                                    
                                  </div>

                                  <div className="flip-card-back">
                                    <h4>{utils.lang["select"]}</h4><br/>
                                    <h3>{p.option.split("/")[0]}</h3>
                                  </div>
                                </div>
                              </div>
                            </label>
                            <br />
                          </div>
                        </div>
                        <br />
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
            {/* The alumn list */}
            {votingType === "general" && (
              <div className="alum-list question" align="center">
                <div>
                  <h2>{alumList.desc}</h2>
                </div>
                <div className="container-fluid">
                  {sendVotingAnimation && (
                    <div className="votingAnimation">
                      <a id="rotator">
                        <img src="https://image.flaticon.com/icons/png/512/91/91848.png" />
                      </a>
                    </div>
                  )}
                  <div className="d-flex align-content-center flex-wrap ">
                    {alumList.options.map((p) => (
                      <div key={p.number} className="p-3">
                        {p.option.split("/")[0]}
                        <label className="checkbox">
                          <input
                            type="checkbox"
                            name={alumList.desc}
                            value={
                              p.option.split("/")[1].replace(" ","") + " " + p.number
                            }
                          />
                          <span className="default"></span>
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
            <div>
              <button id="voteButton" className="btn btn-outline-dark">

                {utils.lang["vote"]}
              </button>
            </div>

          </form>
        </div>
        {utils.alert.lvl ? (
          <div className={"alert " + utils.alert.lvl}>
            <p>{utils.alert.msg}</p>
            <button className=" btn btn-outline-dark " onClick={closeAlert}>
              {
                utils.alert.lvl === "error" || utils.alert.lvl === "errorGeneral" || utils.alert.lvl === "errorPrimary"
                  ? utils.lang["empezar"]
                  : utils.lang["volver"]
              }
            </button>
          </div>
        ) : null}
      </div>
    </div>

  );
};
export default Voting;
