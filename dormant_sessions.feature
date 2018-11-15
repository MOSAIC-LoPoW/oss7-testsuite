Feature: Dormant session

Scenario: Dormant session succeeds for a requester which does unicast requests
    Given an access profile using <channel_class> which does not scan
    And an access profile using <channel_class> which does scan continuously
    And a requester, using the first AP
    And a responder, using the second AP
    And a dormant session registered at the responder for the UID of the requester
    When the requester starts a unicast session to the responder
    Then the requester's session should complete successfully
    And the responder should receive an unsolicited response
    And the requester should receive the dormant session
    And the responders's dormant session should complete successfully

Examples: example1
    | channel_class |
    | lo            |
#    | normal        |
#    | hi            |

Scenario: Dormant session fails for a requester which does broadcast requests
    Given an access profile using <channel_class> which does not scan
    And an access profile using <channel_class> which does scan continuously
    And a requester, using the first AP
    And a responder, using the second AP
    And a dormant session registered at the responder for the UID of the requester
    When the requester starts a broadcast session to the responder
    Then the requester's session should complete successfully
    And the responder should receive an unsolicited response
    And the requester should not receive the dormant session
    # TODO And the responders's dormant session should not complete successfully

Examples: example1
    | channel_class |
    | lo            |
#    | normal        |
#    | hi            |

Scenario: Dormant session times out as expected and fails when no response
    Given an access profile using <channel_class> which does not scan
    And an access profile using <channel_class> which does scan continuously
    And a requester, using the first AP
    And a responder, using the second AP
    And a dormant session registered at the responder for the UID of the requester
    When waiting for the dormant session to time out
    Then the responders's dormant session should not complete successfully

Examples: example1
    | channel_class |
    | lo            |
#    | normal        |
#    | hi            |

Scenario: Dormant session times out as expected and succeeds on response
    Given an access profile using <channel_class> which does not scan
    And an access profile using <channel_class> which does scan continuously
    And a requester, using the first AP
    And a responder, using the second AP
    And a dormant session registered at the responder for the UID of the requester
    When waiting for the dormant session to time out
    Then the responders's dormant session should complete successfully

Examples: example1
    | channel_class |
    | lo            |
#    | normal        |
#    | hi            |