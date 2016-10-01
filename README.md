# FlowAPI

API for optimizing control settings to reach desired flow

===

### How to use
#### Expected input
~~~
{
	"requestedFlow": 2000,
	"numOfControls": 4,
	"floor": 0.05,
	"ceiling": 13.1,
  	"timestamp": "2016-09-01T05:18:29.393",
	"headwater": 26.86,
	"tailwater": 21.1,
	"timeseriesName": "S65D-S-Q"
}
~~~

Definitions:

| Key            | Type    | Definition                                                                                       |
|----------------|---------|--------------------------------------------------------------------------------------------------|
| requestedFlow  | Float   | Desired flow                                                                                     |
| numOfControls  | Integer | How many control units at this location                                                          |
| floor          | Float   | Floor value for control units                                                                    |
| ceiling        | Float   | Ceiling value for control units                                                                  |
| timestamp      | String  | The timestamp to use when calculating flow (optional, if omitted then current time will be used) |
| headwater      | Float   | Headwater value to use when calculating flow                                                     |
| tailwater      | Float   | Tailwater value to use when calculating flow                                                     |
| timeseriesName | String  | Timeseries name for calculating flow                                                             |

===

#### Expected output
~~~
{
  "controlValues": [
    0.8955685133263356,
    0.24467359361774416,
    3.285415835732434,
    1.0560321889739273
  ],
  "actualOutput": 2023.8641593173988,
  "expectedOutput": 2000
}
~~~

Definitions:

| Key            | Type  | Definition                                                                                           |
|----------------|-------|------------------------------------------------------------------------------------------------------|
| controlValues  | Array | An array containing control values that when used to calculate flow will result in the actual output |
| actualOutput   | Float | The flow output to be expected when control values are set to the recommended settings               |
| expectedOutput | Float | The goal flow output requested by the client (the value given in the request)                        |
