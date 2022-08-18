from MobileRobot import MobileRobot
import pytest

# setup variables
setup_position_x = 0
setup_position_y = 10
setup_sensor_noise_threshold = 1


@pytest.fixture
def the_robot():
    return MobileRobot(setup_position_x, setup_position_y, setup_sensor_noise_threshold)


@pytest.mark.init
def test_setup_position(the_robot):
    assert the_robot.position == {"pos_x": setup_position_x, "pos_y": setup_position_y}


@pytest.mark.init
def test_setup_sensor_noise_threshold(the_robot):
    assert the_robot.sensor_noise_threshold == setup_sensor_noise_threshold


@pytest.mark.move
def test_move_result(the_robot):
    move_x = 9
    move_y = 5
    the_robot.move(move_x, move_y)
    assert the_robot.position["pos_x"] == setup_position_x + move_x
    assert the_robot.position["pos_y"] == setup_position_y + move_y


@pytest.mark.move
def test_move_input_handling(the_robot):
    move_x = 9
    move_y = "5"
    with pytest.raises(TypeError):
        the_robot.move(move_x, move_y)


@pytest.mark.move
def test_move_range_exceeded(the_robot):
    move_x = 11
    move_y = 0
    with pytest.raises(ValueError):
        the_robot.move(move_x, move_y)


@pytest.mark.move
def test_move_crossing_borders_x(the_robot):
    move_x = -9
    move_y = 0
    with pytest.raises(ValueError):
        the_robot.move(move_x, move_y)


@pytest.mark.move
def test_move_crossing_borders_y(the_robot):
    move_x = 0
    move_y = -10
    the_robot.move(move_x, move_y)
    with pytest.raises(ValueError):
        the_robot.move(move_x, move_y)


@pytest.mark.SLAM
def test_SLAM_record(the_robot):
    list_of_moves = [(3, 10), (-1, -10), (2, 3)]
    for i in list_of_moves:
        the_robot.move(i[0], i[1])
    assert the_robot.read_SLAM_record() == list_of_moves


@pytest.mark.SLAM
def test_SLAM_calculate_position_change(the_robot):
    list_of_moves = [(3, 10), (-1, -10), (2, 3)]
    for i in list_of_moves:
        the_robot.move(i[0], i[1])
    SLAM_calculate_position_change_output = the_robot.SLAM_calculate_position_change()
    assert SLAM_calculate_position_change_output["x"] == list_of_moves[0][0] + list_of_moves[1][0] + list_of_moves[2][0]
    assert SLAM_calculate_position_change_output["y"] == list_of_moves[0][1] + list_of_moves[1][1] + list_of_moves[2][1]


@pytest.mark.sensor
def test_position_sensor(the_robot):
    position_sensor_output = the_robot.read_position_sensor()
    assert abs(position_sensor_output[0] - setup_position_x) < setup_sensor_noise_threshold
    assert abs(position_sensor_output[1] - setup_position_y) < setup_sensor_noise_threshold


@pytest.mark.sensor
def test_sensor_noise_wrong_threshold(the_robot):
    the_robot.sensor_noise_threshold = "text"
    with pytest.raises(TypeError):
        the_robot.read_position_sensor()
