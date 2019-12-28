from aoc.day_06 import Orbits


def test_orbits():
    data = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\n"
    assert Orbits.from_str(data).root.checksum() == 42


def test_transfers():
    data = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN\n"
    assert Orbits.from_str(data).transfers_between("YOU", "SAN") == 4
