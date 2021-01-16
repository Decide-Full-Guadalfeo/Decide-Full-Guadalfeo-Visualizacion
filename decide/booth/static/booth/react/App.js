import Voting from "./Voting/Voting";
const { useState, useEffect } = React;

const App = () => {

  /*#################################################################*/
  /*############################ LANGUAGES ##########################*/
  /*#################################################################*/

  const en = {
    current: "en",
    prev: "Prev",
    next: "Next",
    vote: "Vote",
    modal_button: "Voting guide",
    modal_title: "Voting guide",
    modal_body: "Welcome to the voting portal of Decide! To register "+
    "your vote, click on the cards, and they will flip. You can only "+
    "choose one per question. If this is a general voting in the final "+
    "question, you can choose more than one, but a maximum of ten, and five men and five women.",
    language_button: "https://images.vexels.com/media/users/3/164598/isolated/preview/ae39cafd26e1b3739a0265ad7e65ebdc-icono-de-idioma-de-la-bandera-de-espa-ntilde-a-by-vexels.png",
    modal_close_button: "Ok, let's go!",
    cand: "Candidate",
    select: "You selected",
    internalError: "Internal error",
    congratulations: "Congratulations! Your vote has been sent.",
    blankError: "Please, do not leave empty questions",
    bigError:"Please, do not leave empty questions.\nIf this is a general voting in the final question, you can choose more than one, but a maximum of ten and five men and five women",
    volver: "Return to index",
    empezar: "Start again"
  };
  const es = {
    current: "es",
    prev: "Previo",
    next: "Siguiente",
    vote: "Votar",
    modal_button: "Guía de votación",
    modal_title: "Guía de votación",
    modal_body: "¡Bienvenido al portal de votaciones de Decide! Para registrar " +
      "tu voto, solo tienes que pulsar en una de las cartas, y esta se " +
      "girará. Solo puedes elegir uno por " +
      "pregunta. Si es una votación general, en la pregunta final puedes elegir más de uno,"+
      " pero un máximo de 10 candidatos, 5 hombres y 5 mujeres.",
    language_button: "https://images.vexels.com/media/users/3/163965/isolated/lists/5bb2c926d53cc59030477ec3ecb6d26a-england-flag-language-icon.png",
    modal_close_button: "Entendido, ¡vamos allá!",
    cand: "Candidato",
    select: "Has elegido",
    internalError: "Error interno",
    congratulations: "¡Enhorabuena! Tu voto ha sido enviado.",
    blankError: "Por favor, no deje preguntas vacías",
    bigError:"Por favor, no deje preguntas vacías.\nSólo se pueden seleccionar 10 alumnos en la lista como máximo, y 5 hombres y mujeres respectivamente.",
    volver: "Volver al inicio",
    empezar: "Empezar de nuevo"

  };

  /*#################################################################*/
  /*####################### UTILITY FUNCTIONS #######################*/
  /*#################################################################*/

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const post = (url, data) => {
    var fdata = {
      body: JSON.stringify(data),
      headers: {
        "content-type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      method: "POST",
    };
    if (votingUserData) {
      fdata.headers["Authorization"] = "Token " + votingUserData.token;
      fdata.headers["auth-token"] = "Token " + votingUserData.token;
    }

    return fetch(url, fdata).then((response) => {
      if (response.status === 200) {
        return response.json();
      } else {
        return Promise.reject(response.statusText);
      }
    });
  };

  const getVotingUserData = () => {
    utils
      .post("/authentication/decide/getVotingUser/")
      .then((res) => {
        setVotingUserData(res);
      })
      .catch((error) => {
        console.log(error);
        window.location.replace('/decide/login')
      });
  };

  const changeLanguage = () => {
    if (lang.current === "es") {
      setLang(en)
    } else {
      setLang(es)
    }
    
  }

  /*#####################################################*/
  /*####################### STATE #######################*/
  /*#####################################################*/

  const [votingUserData, setVotingUserData] = useState(null);
  const [alert, setAlert] = useState({ lvl: null, msg: null });
  const [lang, setLang] = useState(es);

  /*#############################################################*/
  /*####################### FUNCTIONALITY #######################*/
  /*#############################################################*/

  //Run only once
  useEffect(() => {
    getVotingUserData();
  }, []);

  const utils = { alert, setAlert, post, votingUserData, lang, changeLanguage };

  /*####################################################*/
  /*####################### VIEW #######################*/
  /*####################################################*/

  return (
    <div className="App">
      <div></div>
      {votingUserData && <Voting utils={utils} />}
    </div>
  );
};

const domContainer = document.querySelector("#react-root");
ReactDOM.render(<App />, domContainer);
