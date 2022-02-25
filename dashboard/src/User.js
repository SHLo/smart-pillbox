import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import "antd/dist/antd.css";
import { TimePicker } from "antd";
import ListGroup from "react-bootstrap/ListGroup";
import { useState, useEffect } from "react";
import Badge from "react-bootstrap/Badge";
import _ from "lodash";
import { updateUser } from "./db.js";
import Image from "react-bootstrap/Image";
import { BsFillCameraFill } from "react-icons/bs";
import Camera from "./Camera.js";

const IMG_SRC_HEADER = "data:image/jpeg;base64,";

function User(props) {
  console.log(props.user);
  const { user } = props;

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [scheduleTime, setScheduleTime] = useState([]);
  const [imgSrc, setImgSrc] = useState("");
  const [loading, setLoading] = useState(false);

  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    setFirstName(user.first_name);
    setLastName(user.last_name);
    setImgSrc(`${IMG_SRC_HEADER}${user.photo}`);
    setScheduleTime(user.schedule ? user.schedule.time : []);
  }, [user.first_name, user.last_name, user.photo, user.schedule]);

  return _.isEmpty(user) ? (
    <></>
  ) : (
    <>
      <Container>
        <Form>
          <Row className="mb-3">
            <Col md={{ span: 4, offset: 4 }}>
              <Image
                src={imgSrc}
                height="400"
                width="300"
                roundedCircle
              ></Image>
              <Badge
                variant="light"
                bg="light"
                text="dark"
                as={Button}
                pill
                onClick={() => {
                  setShowModal(true);
                }}
              >
                <BsFillCameraFill size={40}></BsFillCameraFill>
              </Badge>
            </Col>
          </Row>

          <Row className="mb-3">
            <Form.Group as={Col} controlId="formGridFirstName">
              <Form.Label>First Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter first name"
                onChange={(e) => setFirstName(e.target.value)}
                value={firstName}
              />
            </Form.Group>

            <Form.Group as={Col} controlId="formGridLastName">
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter first name"
                onChange={(e) => setLastName(e.target.value)}
                value={lastName}
              />
            </Form.Group>
          </Row>
          <Row>
            <Col md={{ span: 4, offset: 4 }}>
              <ListGroup as={Col}>
                {scheduleTime.map((time, i) => (
                  <ListGroup.Item
                    className="d-flex justify-content-between"
                    key={i}
                  >
                    {time}
                    <Badge
                      variant="light"
                      bg="light"
                      text="dark"
                      as={Button}
                      pill
                      onClick={() =>
                        setScheduleTime(
                          scheduleTime.filter((tbd) => tbd !== time)
                        )
                      }
                    >
                      x
                    </Badge>
                  </ListGroup.Item>
                ))}
              </ListGroup>
              <TimePicker
                className="mt-3"
                format={"HH:mm"}
                onChange={(setTime) => {
                  const timeStr = setTime.format("hh:mm");
                  if (!scheduleTime.includes(timeStr)) {
                    const newScheduleTime = [...scheduleTime, timeStr].sort();
                    setScheduleTime(newScheduleTime);
                  }
                }}
              />
            </Col>
          </Row>

          <Button
            variant="primary"
            disabled={loading}
            onClick={async () => {
              setLoading(true);
              const userUpdated = {
                ...user,
                first_name: firstName,
                last_name: lastName,
                schedule: { time: scheduleTime },
                photo: imgSrc.substring(IMG_SRC_HEADER.length),
              };
              await updateUser(userUpdated);
              setLoading(false);
            }}
          >
            Update
          </Button>
        </Form>
      </Container>
      <Camera
        showModal={showModal}
        setShowModal={setShowModal}
        imgSrc={imgSrc}
        setImgSrc={setImgSrc}
      ></Camera>
    </>
  );
}

export default User;
