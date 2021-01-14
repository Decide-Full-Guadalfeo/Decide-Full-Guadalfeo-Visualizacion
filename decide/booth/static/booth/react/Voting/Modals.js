//NO FUNCIONA

const { useState, useEffect } = React;

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
        <button >Display Modal</button>
        <Modal show={isOpen} onHide={hideModal}>
        onClick={showModal}
          <Modal.Header>
            <Modal.Title>Hi</Modal.Title>
          </Modal.Header>
          <Modal.Body>The body</Modal.Body>
          <Modal.Footer>
            <button onClick={hideModal}>Cancel</button>
            <button>Save</button>
          </Modal.Footer>
    </Modal>
      </div>
    );
};
export default Modals;