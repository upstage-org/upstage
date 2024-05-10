export default {
    "scalars": [
        2,
        5,
        6,
        9,
        10,
        11,
        15,
        19,
        23,
        26,
        27,
        28,
        33,
        37,
        39
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
            "mediaTypes": [
                3,
                {
                    "sort": [
                        11,
                        "[AssetTypeSortEnum]"
                    ],
                    "before": [
                        6
                    ],
                    "after": [
                        6
                    ],
                    "first": [
                        10
                    ],
                    "last": [
                        10
                    ]
                }
            ],
            "tags": [
                12,
                {
                    "sort": [
                        15,
                        "[TagSortEnum]"
                    ],
                    "before": [
                        6
                    ],
                    "after": [
                        6
                    ],
                    "first": [
                        10
                    ],
                    "last": [
                        10
                    ]
                }
            ],
            "users": [
                16,
                {
                    "active": [
                        5
                    ],
                    "sort": [
                        19,
                        "[UserSortEnum]"
                    ],
                    "before": [
                        6
                    ],
                    "after": [
                        6
                    ],
                    "first": [
                        10
                    ],
                    "last": [
                        10
                    ]
                }
            ],
            "media": [
                20,
                {
                    "id": [
                        2
                    ],
                    "nameLike": [
                        6
                    ],
                    "createdBetween": [
                        27,
                        "[Date]"
                    ],
                    "fileLocation": [
                        6
                    ],
                    "mediaTypes": [
                        6,
                        "[String]"
                    ],
                    "owners": [
                        6,
                        "[String]"
                    ],
                    "stages": [
                        10,
                        "[Int]"
                    ],
                    "tags": [
                        6,
                        "[String]"
                    ],
                    "sort": [
                        28,
                        "[AssetSortEnum]"
                    ],
                    "before": [
                        6
                    ],
                    "after": [
                        6
                    ],
                    "first": [
                        10
                    ],
                    "last": [
                        10
                    ]
                }
            ],
            "stages": [
                29,
                {
                    "id": [
                        2
                    ],
                    "nameLike": [
                        6
                    ],
                    "createdBetween": [
                        27,
                        "[Date]"
                    ],
                    "fileLocation": [
                        6
                    ],
                    "owners": [
                        6,
                        "[String]"
                    ],
                    "sort": [
                        33,
                        "[StageSortEnum]"
                    ],
                    "before": [
                        6
                    ],
                    "after": [
                        6
                    ],
                    "first": [
                        10
                    ],
                    "last": [
                        10
                    ]
                }
            ],
            "adminPlayers": [
                34,
                {
                    "id": [
                        2
                    ],
                    "usernameLike": [
                        6
                    ],
                    "createdBetween": [
                        27,
                        "[Date]"
                    ],
                    "role": [
                        10
                    ],
                    "sort": [
                        37,
                        "[AdminPlayerSortEnum]"
                    ],
                    "before": [
                        6
                    ],
                    "after": [
                        6
                    ],
                    "first": [
                        10
                    ],
                    "last": [
                        10
                    ]
                }
            ],
            "whoami": [
                18
            ],
            "notifications": [
                38
            ],
            "voices": [
                40
            ],
            "__typename": [
                6
            ]
        },
        "Node": {
            "id": [
                2
            ],
            "on_AssetType": [
                8
            ],
            "on_Tag": [
                14
            ],
            "on_User": [
                18
            ],
            "on_Asset": [
                22
            ],
            "on_AssetUsage": [
                25
            ],
            "on_Stage": [
                31
            ],
            "on_AdminPlayer": [
                36
            ],
            "on_Notification": [
                38
            ],
            "on_Voice": [
                40
            ],
            "__typename": [
                6
            ]
        },
        "ID": {},
        "AssetTypeConnection": {
            "pageInfo": [
                4
            ],
            "edges": [
                7
            ],
            "__typename": [
                6
            ]
        },
        "PageInfo": {
            "hasNextPage": [
                5
            ],
            "hasPreviousPage": [
                5
            ],
            "startCursor": [
                6
            ],
            "endCursor": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "Boolean": {},
        "String": {},
        "AssetTypeEdge": {
            "node": [
                8
            ],
            "cursor": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "AssetType": {
            "id": [
                2
            ],
            "name": [
                6
            ],
            "description": [
                6
            ],
            "fileLocation": [
                6
            ],
            "createdOn": [
                9
            ],
            "dbId": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "DateTime": {},
        "Int": {},
        "AssetTypeSortEnum": {},
        "TagConnection": {
            "pageInfo": [
                4
            ],
            "edges": [
                13
            ],
            "__typename": [
                6
            ]
        },
        "TagEdge": {
            "node": [
                14
            ],
            "cursor": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "Tag": {
            "id": [
                2
            ],
            "name": [
                6
            ],
            "color": [
                6
            ],
            "createdOn": [
                9
            ],
            "dbId": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "TagSortEnum": {},
        "UserConnection": {
            "pageInfo": [
                4
            ],
            "edges": [
                17
            ],
            "__typename": [
                6
            ]
        },
        "UserEdge": {
            "node": [
                18
            ],
            "cursor": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "User": {
            "id": [
                2
            ],
            "username": [
                6
            ],
            "password": [
                6
            ],
            "email": [
                6
            ],
            "binName": [
                6
            ],
            "role": [
                10
            ],
            "firstName": [
                6
            ],
            "lastName": [
                6
            ],
            "displayName": [
                6
            ],
            "active": [
                5
            ],
            "createdOn": [
                9
            ],
            "firebasePushnotId": [
                6
            ],
            "deactivatedOn": [
                9
            ],
            "uploadLimit": [
                10
            ],
            "intro": [
                6
            ],
            "canSendEmail": [
                5
            ],
            "lastLogin": [
                9
            ],
            "dbId": [
                10
            ],
            "roleName": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "UserSortEnum": {},
        "AssetConnection": {
            "pageInfo": [
                4
            ],
            "edges": [
                21
            ],
            "totalCount": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "AssetEdge": {
            "node": [
                22
            ],
            "cursor": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "Asset": {
            "id": [
                2
            ],
            "name": [
                6
            ],
            "assetTypeId": [
                10
            ],
            "ownerId": [
                10
            ],
            "description": [
                6
            ],
            "fileLocation": [
                6
            ],
            "createdOn": [
                9
            ],
            "updatedOn": [
                9
            ],
            "size": [
                23
            ],
            "copyrightLevel": [
                10
            ],
            "assetType": [
                8
            ],
            "owner": [
                18
            ],
            "stages": [
                24
            ],
            "tags": [
                6
            ],
            "permissions": [
                25
            ],
            "dbId": [
                10
            ],
            "src": [
                6
            ],
            "privilege": [
                26
            ],
            "sign": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "Float": {},
        "AssignedStage": {
            "id": [
                10
            ],
            "name": [
                6
            ],
            "url": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "AssetUsage": {
            "id": [
                2
            ],
            "assetId": [
                10
            ],
            "userId": [
                10
            ],
            "approved": [
                5
            ],
            "seen": [
                5
            ],
            "note": [
                6
            ],
            "createdOn": [
                9
            ],
            "user": [
                18
            ],
            "asset": [
                22
            ],
            "__typename": [
                6
            ]
        },
        "Previlege": {},
        "Date": {},
        "AssetSortEnum": {},
        "StageConnection": {
            "pageInfo": [
                4
            ],
            "edges": [
                30
            ],
            "totalCount": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "StageEdge": {
            "node": [
                31
            ],
            "cursor": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "Stage": {
            "id": [
                2
            ],
            "name": [
                6
            ],
            "description": [
                6
            ],
            "ownerId": [
                10
            ],
            "fileLocation": [
                6
            ],
            "createdOn": [
                9
            ],
            "lastAccess": [
                9
            ],
            "cover": [
                6
            ],
            "visibility": [
                6
            ],
            "status": [
                6
            ],
            "owner": [
                18
            ],
            "attributes": [
                32
            ],
            "dbId": [
                10
            ],
            "permission": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "StageAttributes": {
            "id": [
                23
            ],
            "stageId": [
                10
            ],
            "name": [
                6
            ],
            "description": [
                6
            ],
            "createdOn": [
                9
            ],
            "stage": [
                31
            ],
            "__typename": [
                6
            ]
        },
        "StageSortEnum": {},
        "AdminPlayerConnection": {
            "pageInfo": [
                4
            ],
            "edges": [
                35
            ],
            "totalCount": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "AdminPlayerEdge": {
            "node": [
                36
            ],
            "cursor": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "AdminPlayer": {
            "id": [
                2
            ],
            "username": [
                6
            ],
            "password": [
                6
            ],
            "email": [
                6
            ],
            "binName": [
                6
            ],
            "role": [
                10
            ],
            "firstName": [
                6
            ],
            "lastName": [
                6
            ],
            "displayName": [
                6
            ],
            "active": [
                5
            ],
            "createdOn": [
                9
            ],
            "firebasePushnotId": [
                6
            ],
            "deactivatedOn": [
                9
            ],
            "uploadLimit": [
                10
            ],
            "intro": [
                6
            ],
            "canSendEmail": [
                5
            ],
            "lastLogin": [
                9
            ],
            "dbId": [
                10
            ],
            "permission": [
                6
            ],
            "roleName": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "AdminPlayerSortEnum": {},
        "Notification": {
            "id": [
                2
            ],
            "type": [
                39
            ],
            "mediaUsage": [
                25
            ],
            "__typename": [
                6
            ]
        },
        "NotificationType": {},
        "Voice": {
            "id": [
                2
            ],
            "voice": [
                41
            ],
            "avatar": [
                22
            ],
            "__typename": [
                6
            ]
        },
        "VoiceOutput": {
            "voice": [
                6
            ],
            "variant": [
                6
            ],
            "pitch": [
                10
            ],
            "speed": [
                10
            ],
            "amplitude": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "Mutation": {
            "calcSizes": [
                43
            ],
            "deleteMedia": [
                44,
                {
                    "id": [
                        2,
                        "ID!"
                    ]
                }
            ],
            "uploadFile": [
                45,
                {
                    "base64": [
                        6,
                        "String!"
                    ],
                    "filename": [
                        6,
                        "String!"
                    ]
                }
            ],
            "saveMedia": [
                46,
                {
                    "input": [
                        47,
                        "SaveMediaInput!"
                    ]
                }
            ],
            "authUser": [
                50,
                {
                    "password": [
                        6
                    ],
                    "username": [
                        6
                    ]
                }
            ],
            "refreshUser": [
                51,
                {
                    "refreshToken": [
                        6
                    ]
                }
            ],
            "confirmPermission": [
                52,
                {
                    "approved": [
                        5
                    ],
                    "id": [
                        2
                    ]
                }
            ],
            "requestPermission": [
                53,
                {
                    "assetId": [
                        2
                    ],
                    "note": [
                        6
                    ]
                }
            ],
            "quickAssignMutation": [
                54,
                {
                    "id": [
                        2
                    ],
                    "stageId": [
                        10
                    ]
                }
            ],
            "updateStatus": [
                55,
                {
                    "stageId": [
                        2,
                        "ID!"
                    ]
                }
            ],
            "updateVisibility": [
                56,
                {
                    "stageId": [
                        2,
                        "ID!"
                    ]
                }
            ],
            "updateUser": [
                57,
                {
                    "inbound": [
                        58,
                        "UpdateUserInput!"
                    ]
                }
            ],
            "deleteUser": [
                59,
                {
                    "inbound": [
                        60,
                        "DeleteUserInput!"
                    ]
                }
            ],
            "batchUserCreation": [
                61,
                {
                    "stageIds": [
                        10,
                        "[Int]"
                    ],
                    "users": [
                        62,
                        "[BatchUserInput]!"
                    ]
                }
            ],
            "sendEmail": [
                63,
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
            "changePassword": [
                64,
                {
                    "inbound": [
                        65,
                        "ChangePasswordInput!"
                    ]
                }
            ],
            "__typename": [
                6
            ]
        },
        "CalcSizes": {
            "size": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "DeleteMedia": {
            "success": [
                5
            ],
            "message": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "UploadFile": {
            "url": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "SaveMedia": {
            "asset": [
                22
            ],
            "__typename": [
                6
            ]
        },
        "SaveMediaInput": {
            "name": [
                6
            ],
            "urls": [
                6
            ],
            "mediaType": [
                6
            ],
            "id": [
                2
            ],
            "copyrightLevel": [
                10
            ],
            "owner": [
                6
            ],
            "userIds": [
                10
            ],
            "stageIds": [
                10
            ],
            "tags": [
                6
            ],
            "w": [
                10
            ],
            "h": [
                10
            ],
            "note": [
                6
            ],
            "voice": [
                48
            ],
            "link": [
                49
            ],
            "__typename": [
                6
            ]
        },
        "AvatarVoiceInput": {
            "voice": [
                6
            ],
            "variant": [
                6
            ],
            "pitch": [
                10
            ],
            "speed": [
                10
            ],
            "amplitude": [
                10
            ],
            "__typename": [
                6
            ]
        },
        "LinkInput": {
            "url": [
                6
            ],
            "blank": [
                5
            ],
            "effect": [
                5
            ],
            "__typename": [
                6
            ]
        },
        "AuthMutation": {
            "accessToken": [
                6
            ],
            "refreshToken": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "RefreshMutation": {
            "newToken": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "ConfirmPermission": {
            "success": [
                5
            ],
            "message": [
                6
            ],
            "permissions": [
                25
            ],
            "__typename": [
                6
            ]
        },
        "RequestPermission": {
            "success": [
                5
            ],
            "__typename": [
                6
            ]
        },
        "QuickAssignMutation": {
            "success": [
                5
            ],
            "message": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "UpdateAttributeStatus": {
            "result": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "UpdateAttributeVisibility": {
            "result": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "UpdateUser": {
            "user": [
                36
            ],
            "__typename": [
                6
            ]
        },
        "UpdateUserInput": {
            "username": [
                6
            ],
            "password": [
                6
            ],
            "email": [
                6
            ],
            "binName": [
                6
            ],
            "role": [
                10
            ],
            "firstName": [
                6
            ],
            "lastName": [
                6
            ],
            "displayName": [
                6
            ],
            "active": [
                5
            ],
            "firebasePushnotId": [
                6
            ],
            "uploadLimit": [
                10
            ],
            "intro": [
                6
            ],
            "id": [
                2
            ],
            "__typename": [
                6
            ]
        },
        "DeleteUser": {
            "success": [
                5
            ],
            "__typename": [
                6
            ]
        },
        "DeleteUserInput": {
            "username": [
                6
            ],
            "password": [
                6
            ],
            "email": [
                6
            ],
            "binName": [
                6
            ],
            "role": [
                10
            ],
            "firstName": [
                6
            ],
            "lastName": [
                6
            ],
            "displayName": [
                6
            ],
            "active": [
                5
            ],
            "firebasePushnotId": [
                6
            ],
            "uploadLimit": [
                10
            ],
            "intro": [
                6
            ],
            "id": [
                2
            ],
            "__typename": [
                6
            ]
        },
        "BatchUserCreation": {
            "users": [
                36
            ],
            "__typename": [
                6
            ]
        },
        "BatchUserInput": {
            "username": [
                6
            ],
            "email": [
                6
            ],
            "password": [
                6
            ],
            "__typename": [
                6
            ]
        },
        "SendEmail": {
            "success": [
                5
            ],
            "__typename": [
                6
            ]
        },
        "ChangePassword": {
            "success": [
                5
            ],
            "__typename": [
                6
            ]
        },
        "ChangePasswordInput": {
            "id": [
                2
            ],
            "oldPassword": [
                6
            ],
            "newPassword": [
                6
            ],
            "__typename": [
                6
            ]
        }
    }
}