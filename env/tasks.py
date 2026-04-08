TASKS = {
    "easy": {
        "tickets": [
            {
                "id": "T1",
                "message": "I was charged twice for my subscription",
                "expected_priority": "high",
                "expected_department": "billing",
                "ideal_response": "We apologize for the duplicate charge. Our billing team will review and process a refund."
            }
        ]
    },
    "medium": {
        "tickets": [
            {
                "id": "T2",
                "message": "App crashes when uploading files",
                "expected_priority": "high",
                "expected_department": "tech",
                "ideal_response": "We understand the issue and our technical team is investigating the crash."
            },
            {
                "id": "T3",
                "message": "Need invoice for last month",
                "expected_priority": "medium",
                "expected_department": "billing",
                "ideal_response": "We will share your invoice shortly via email."
            }
        ]
    },
    "hard": {
        "tickets": [
            {
                "id": "T4",
                "message": "Account locked and billing issue",
                "expected_priority": "high",
                "expected_department": "tech",
                "ideal_response": "We are unlocking your account and reviewing the billing concern."
            }
        ]
    }
}
