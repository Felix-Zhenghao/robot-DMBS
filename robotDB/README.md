# Ten example queries
- Get task that may potentially need more high-quality teleoperation: Compute the success rate of demonstrations labelled with "robot_generated" of different tasks. Show the task name and success rate. Order the success rate ascendingly.
```SQL
SELECT 
    d.taskName,
    d.robotModel,
    ROUND(SUM(d.success) / COUNT(*) * 100, 2) AS successRate
FROM 
    Demonstrations d
WHERE 
    d.label = 'robot_generated'
GROUP BY 
    d.taskName,
    d.robotModel
ORDER BY 
    successRate ASC;
```
- Get experts: Find the demonstrator who is experienced with the robot
```SQL
SELECT 
    demonstratorID
FROM 
    Experience
WHERE 
    robotModel = 'IIWA' 
    AND experience = 'expert';
```

- Get demonstrations from expert demonstrators: show demo id of IIWA robot that is teleoperated by IIWA experts.
```SQL
SELECT 
    d.demoID
FROM 
    Demonstrations d
JOIN 
    Experience e
ON 
    d.demonstratorID = e.demonstratorID
WHERE 
    e.robotModel = 'IIWA' 
    AND e.experience = 'expert';
```

- Good teleoperators for challenging tasks: Find the demonstrator with highest data generation success rate for hard tasks involving subtasks with deformable relative object.
```SQL
SELECT 
    d.demonstratorID,
    ROUND(SUM(d.success) / COUNT(*) * 100, 2) AS successRate
FROM 
    Demonstrations d
JOIN 
    Tasks t
ON 
    d.taskName = t.taskName
JOIN 
    Subtasks st
ON 
    t.taskName = st.taskName
JOIN 
    Objects o
ON 
    st.relativeObject = o.objectName
WHERE 
    t.difficulty = 'hard'
    AND d.label = 'robot_generated'
    AND o.classification = 'deformable'
GROUP BY 
    d.demonstratorID
ORDER BY 
    successRate DESC
LIMIT 1;
```

- Get all long-horizon tasks and show all subtask descriptions
```SQL
SELECT 
    st.subtaskDescription,
    t.taskName
FROM 
    Subtasks st
JOIN 
    Tasks t
ON 
    st.taskName = t.taskName
WHERE 
    t.taskType = 'long_horizon';
```
- Good robot data from good demonstrators: Get all success robot generated trajectories of the contact-rich tasks that is teleoperated by experienced (intermediate or expert) demonstrators of the corresponding robot model
```SQL
SELECT 
    d.demoID
FROM 
    Demonstrations d
JOIN 
    Tasks t
ON 
    d.taskName = t.taskName
JOIN 
    Experience e
ON 
    d.demonstratorID = e.demonstratorID AND d.robotModel = e.robotModel
WHERE 
    t.taskType = 'contact_rich'
    AND d.label = 'robot_generated'
    AND d.success = TRUE
    AND e.experience IN ('intermediate', 'expert');
```
- Inspect the failure mode: Get all failed trajectory of the task
```SQL
SELECT 
    demoID
FROM 
    Demonstrations
WHERE 
    taskName = 'Coffee'
    AND success = FALSE;
```
- Compose the simulation environment: Get the object position and randomization range of a task involving subtask with relative object being rigid type.
```SQL
SELECT 
    ot.objectPositionX, 
    ot.objectPositionY, 
    ot.objectPositionZ, 
    ot.randomizationRange
FROM 
    Subtasks st
JOIN 
    Objects o
ON 
    st.relativeObject = o.objectName
JOIN 
    ObjectTasks ot
ON 
    st.taskName = ot.taskName
WHERE 
    o.classification = 'rigid';
```
- Unqualified expert demonstrators: Get demonstrator that is an 'expert' with 'UR5e' robot, but the UR5e trajectories generated from that demonstrator's demos have a success rate less than 0.3.
```SQL
SELECT 
    e.demonstratorID
FROM 
    Experience e
JOIN 
    Robots r
ON 
    e.robotModel = r.model
JOIN 
    Demonstrations d
ON 
    e.demonstratorID = d.demonstratorID AND e.robotModel = d.robotModel
WHERE 
    e.robotModel = 'UR5e'
    AND e.experience = 'expert'
    AND d.label = 'robot_generated'
GROUP BY 
    e.demonstratorID
HAVING 
    SUM(d.success) / COUNT(*) < 0.3;
```

- Too easy tasks labelled as hard:
```SQL 
SELECT 
    t.taskName
FROM 
    Tasks t
JOIN 
    Demonstrations d
ON 
    t.taskName = d.taskName
WHERE 
    t.difficulty = 'hard' 
    AND d.label = 'robot_generated'
GROUP BY 
    t.taskName
HAVING 
    MIN(d.success) > 0.7;
```

# Some constants
```python
ALL_ENVIRONMENTS = ['Lift', 'Stack', 'NutAssembly', 'NutAssemblySingle', 'NutAssemblySquare', 'NutAssemblyRound', 'PickPlace', 'PickPlaceSingle', 'PickPlaceMilk', 'PickPlaceBread', 'PickPlaceCereal', 'PickPlaceCan', 'Door', 'Wipe', 'ToolHang', 'TwoArmLift', 'TwoArmPegInHole', 'TwoArmHandover', 'TwoArmTransport', 'ToolUseEnvBase', 'ToolUseEnv', 'HammerPlaceEnv', 'KitchenEnv', 'MultitaskKitchenDomain', 'SingleArmEnv_MG', 'Threading', 'Threading_D0', 'Threading_D1', 'Threading_D2', 'Coffee', 'Coffee_D0', 'Coffee_D1', 'Coffee_D2', 'CoffeePreparation', 'CoffeePreparation_D0', 'CoffeePreparation_D1', 'ThreePieceAssembly', 'ThreePieceAssembly_D0', 'ThreePieceAssembly_D1', 'ThreePieceAssembly_D2', 'MugCleanup', 'MugCleanup_D0', 'MugCleanup_D1', 'MugCleanup_O1', 'MugCleanup_O2', 'Stack_D0', 'Stack_D1', 'StackThree', 'StackThree_D0', 'StackThree_D1', 'NutAssembly_D0', 'Square_D0', 'Square_D1', 'Square_D2', 'PickPlace_D0', 'HammerCleanup_D0', 'HammerCleanup_D1', 'Kitchen_D0', 'Kitchen_D1']
```

```python
ALL_ENV_INTERFACE = ['RobosuiteInterface', 'MG_Coffee', 'MG_Threading', 'MG_ThreePieceAssembly', 'MG_Square', 'MG_Stack', 'MG_StackThree', 'MG_HammerCleanup', 'MG_MugCleanup', 'MG_NutAssembly', 'MG_PickPlace', 'MG_Kitchen', 'MG_CoffeePreparation']
```

```python
ALL_SINGLE_ARM_ROBOTS = ["Panda", "Sawyer", "IIWA", "UR5e", "Jaco", "Kinova3"]
```
