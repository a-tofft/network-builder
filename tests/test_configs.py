#!/usr/bin/env python

from pybatfish.client.commands import *

# from pybatfish.client.session import Session
from pybatfish.question import load_questions
from pybatfish.client.asserts import (
    assert_no_duplicate_router_ids,
    assert_no_incompatible_bgp_sessions,
    assert_no_incompatible_ospf_sessions,
    assert_no_unestablished_bgp_sessions,
)

from rich.console import Console

console = Console(color_system="truecolor")


def test_duplicate_rtr_ids(snap):
    """Testing for duplicate router IDs"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for duplicate router IDs[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_duplicate_router_ids(
        snapshot=snap,
        protocols={"ospf", "bgp"},
    )
    console.print(
        ":green_heart: [bold green]No duplicate router IDs found[/bold green] :green_heart:"
    )


def test_bgp_compatibility(snap):
    """Testing for incompatible BGP sessions"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_bgp_sessions(
        snapshot=snap,
    )
    console.print(
        ":green_heart: [bold green]All BGP sessions compatible![/bold green] :green_heart:"
    )


def test_ospf_compatibility(snap):
    """Testing for incompatible OSPF sessions"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for incompatible OSPF sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_incompatible_ospf_sessions(
        snapshot=snap,
    )
    console.print(
        ":green_heart: [bold green]All OSPF sessions compatible![/bold green] :green_heart:"
    )


def test_bgp_unestablished(snap):
    """Testing for BGP sessions that are not established"""
    console.print(
        ":white_exclamation_mark: [bold yellow]Testing for unestablished BGP sessions[/bold yellow] :white_exclamation_mark:"
    )
    assert_no_unestablished_bgp_sessions(
        snapshot=snap,
    )
    console.print(
        ":green_heart: [bold green]All BGP sessions are established![/bold green] :green_heart:"
    )


def main():
    """init all the things"""
    NETWORK_NAME = "NETWORK_BUILDER_LAB"
    SNAPSHOT_NAME = "Generated_Configs"
    SNAPSHOT_DIR = "./network_builder/"  # '../../networks/example'
    BF_SERVICE_IP = "localhost"

    # Define batfish service location
    bf_session.host = BF_SERVICE_IP

    load_questions()
    bf_set_network(NETWORK_NAME)
    init_snap = bf_init_snapshot(SNAPSHOT_DIR, name=SNAPSHOT_NAME, overwrite=True)

    # Perform Tests
    test_duplicate_rtr_ids(init_snap)
    test_bgp_compatibility(init_snap)
    test_ospf_compatibility(init_snap)
    test_bgp_unestablished(init_snap)


s
if __name__ == "__main__":
    main()
