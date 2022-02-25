import { useRef, useCallback } from "react";
import { BsFillCameraFill } from "react-icons/bs";
import Modal from "react-bootstrap/Modal";
import Webcam from "react-webcam";
import Button from "react-bootstrap/Button";

function Camera(props) {
  const { showModal, setShowModal, imgSrc, setImgSrc } = props;

  const webcamRef = useRef(null);

  const capture = useCallback(() => {
    const currentImageSrc = webcamRef.current.getScreenshot();
    setImgSrc(currentImageSrc);
  }, [webcamRef, setImgSrc]);

  return (
    <Modal show={showModal} onHide={() => setShowModal(false)}>
      <Modal.Header closeButton>
        <Modal.Title>Take a new picture</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div className="d-flex justify-content-center">
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            width="300"
            height="400"
            className="d-flex justify-content-center"
            videoConstraints={{ width: 300, height: 400 }}
          />
        </div>
        <div className="d-flex justify-content-center m-2">
          <Button onClick={capture} height="20">
            <BsFillCameraFill size={40}></BsFillCameraFill>
          </Button>
        </div>
        <div className="d-flex justify-content-center">
          <img src={imgSrc} width="300" height="400" alt="current" />
        </div>
      </Modal.Body>
    </Modal>
  );
}

export default Camera;
