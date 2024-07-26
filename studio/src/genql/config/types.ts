export default {
    "scalars": [
        2,
        4,
        6,
        7
    ],
    "types": {
        "Query": {
            "node": [
                1,
                {
                    "id": [
                        2,
                        "ID!"
                    ]
                }
            ],
            "nginx": [
                3
            ],
            "system": [
                5
            ],
            "foyer": [
                8
            ],
            "__typename": [
                6
            ]
        },
        "Node": {
            "id": [
                2
            ],
            "__typename": [
                6
            ]
        },
        "ID": {},
        "NginxConfig": {
            "uploadLimit": [
                4
            ],
            "__typename": [
                6
            ]
        },
        "Int": {},
        "SystemConfig": {
            "termsOfService": [
                6
            ],
            "manual": [
                6
            ],
            "esp": [
                6
            ],
            "enableDonate": [
                7
            ],
            "__typename": [
                6
            ]
        },
        "String": {},
        "Boolean": {},
        "FoyerConfig": {
            "title": [
                6
            ],
            "description": [
                6
            ],
            "menu": [
                6
            ],
            "showRegistration": [
                7
            ],
            "__typename": [
                6
            ]
        },
        "Mutation": {
            "updateTermsOfService": [
                10,
                {
                    "url": [
                        6,
                        "String!"
                    ]
                }
            ],
            "saveConfig": [
                11,
                {
                    "name": [
                        6,
                        "String!"
                    ],
                    "value": [
                        6,
                        "String!"
                    ]
                }
            ],
            "sendEmail": [
                12,
                {
                    "bcc": [
                        6
                    ],
                    "body": [
                        6,
                        "String!"
                    ],
                    "recipients": [
                        6,
                        "String!"
                    ],
                    "subject": [
                        6,
                        "String!"
                    ]
                }
            ],
            "__typename": [
                6
            ]
        },
        "UpdateTermsOfService": {
            "url": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "SaveConfig": {
            "success": [
                7
            ],
            "__typename": [
                6
            ]
        },
        "SendEmail": {
            "success": [
                7
            ],
            "__typename": [
                6
            ]
        }
    }
}