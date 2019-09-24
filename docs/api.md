# tahskr API


## Create a User

![](https://img.shields.io/badge/POST-%2Fauth-5C5C5C?style=flat-square&labelColor=F4982B)

#### URL Parameters

None

#### Data Parameters

| Name         | Required? | Details                        |
| ------------ | --------- | ------------------------------ |
| emailAddress | Yes       | Must be a valid email address. |
| password     | Yes       |                                |

#### Responses

| Code             | Body Content          |
| ---------------- | --------------------- |
| 200 OK           | A user object         |
| 400 Client Error | A message explaining. |

----

## Get To-Dos

![](https://img.shields.io/badge/GET-%2Ftodo-5C5C5C?style=flat-square&labelColor=4DC292)

...