# Quiet Mind
---
Autism self-stimming behavior tracking, alerting, and analysis.
Visualization

### Overall challenge:


Make it personal. Using sponsor technology and your unique skills, build something you're passionate about that will forster better health for your family, friends, community, or the world.

### Technologies
NodeJS, ios, fitbit app.

### Target Sponsors

General best HackHLTH prize for promising company idea.
Fitbit - Option 1 and 3: Fitbit app for collecting accel and gyro data.
Softheon - in the event of a stimming event for the child, the parent can confirm or respond to the event with a dynamic survey based on the actual event. This data would be stored using the softeon enterprise api.

### Concept

Use acceleromoter and gyroscope data to characterize and track your child's abnormal behavior action quantitatively.

Each individual has a unique stimming pattern. We use machine learning to train off of the child's specific pattern of stimming to have an accurate model.

Clinician can review data. Parent has the opportunity to take action if there's stimming occurring to ensure that consistent intervention with the child is taken. Without consistency, a child's behavior or stimming behavior is less likely to improve over time (citation needed).


### How we address FDA approval:
App doesn't do diagnosing or dosing.
App allows insight into behavior outside of direct parental or clinician attention. No potential harm 

### Server (API) Notes

#### Uploading data


The POST endpoint for `/predict` expect lists of data entries in the following body format. You can also simultaneously insert the data by setting insert=True.

<pre>
post_data = {
    'userId': XXXXXXXXXX,
    'insert': true,
    'accel': [
        {
            'userId': XXXXXXXXXX // user id code
            'x': 1, // floating point value
            'y': 2, // floating point value
            'z': 3, // floating point value
            'timestamp': XXXXXXXXX // (timestamp in ms)
        },
        ...
    ],
    'gyro': [
        {
            'userId': XXXXXXXXXX // user id code
            'x': 1, // floating point value
            'y': 2, // floating point value
            'z': 3, // floating point value
            'timestamp': XXXXXXXXX // (timestamp in ms)
        },
        ...
    ]
}
</pre>


The POST endpoints for `/accel` and `/gyro` expect lists of data entries in the following body format.
<pre>
post_data = {
    'userId': XXXXXXXXXX,
    'data': [
        {
            'userId': XXXXXXXXXX // user id code
            'x': 1, // floating point value
            'y': 2, // floating point value
            'z': 3, // floating point value
            'timestamp': XXXXXXXXX // (timestamp in ms)
        },
        ...
    ]
}
</pre>

#### Retrieving time-windowed data
The GET endpoints for `/accel` and `/gyro` expect the following query params:
`startTime=<timestampMS>`
`endTime=<timestampMS>`
`userId=<userId>`

#### Retrieving all data

There are also GET endpoints for all data:<br/>
* `/accel/all`
* `/gyro/all`
* `/stim/all`

with a userId query param.


### Dev Notes

### Useful Libaries
* https://github.com/Pr0Ger/PyAPNs2
* http://sqlalchemy-utils.readthedocs.io/en/latest/range_data_types.html
* http://flask-sqlalchemy.pocoo.org/2.3/quickstart/




