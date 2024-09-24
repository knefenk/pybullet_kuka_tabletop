import pybullet as p
import pybullet_data
import time
import random
import math

# Initialize PyBullet
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)

# Load plane and table
planeId = p.loadURDF("plane.urdf")
tableId = p.loadURDF("table/table.urdf", [0, 0, 0])

# Load Kuka KR210 robot arm
robotStartPos = [0, 0.2, 0.6]
robotStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
robotId = p.loadURDF("kuka_iiwa/model.urdf", robotStartPos, robotStartOrientation, useFixedBase=True)

# Define colors
COLORS = {
    "red": [1, 0, 0, 1],
    "green": [0, 1, 0, 1],
    "blue": [0, 0, 1, 1],
    "yellow": [1, 1, 0, 1],
    "purple": [0.5, 0, 0.5, 1],
    "orange": [1, 0.65, 0, 1],
}

# Define object types
OBJECT_TYPES = ["cube", "sphere", "cylinder"]

def create_random_object(position):
    color = random.choice(list(COLORS.values()))
    obj_type = random.choice(OBJECT_TYPES)
    
    if obj_type == "cube":
        size = 0.05
        visualShapeId = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=[size/2]*3, rgbaColor=color)
        collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=[size/2]*3)
    elif obj_type == "sphere":
        size = 0.05
        visualShapeId = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=size/2, rgbaColor=color)
        collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=size/2)
    else:  # cylinder
        radius = 0.025
        height = 0.05
        visualShapeId = p.createVisualShape(shapeType=p.GEOM_CYLINDER, radius=radius, length=height, rgbaColor=color)
        collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_CYLINDER, radius=radius, height=height)

    objectId = p.createMultiBody(baseMass=0.1,
                                 baseInertialFramePosition=[0, 0, 0],
                                 baseCollisionShapeIndex=collisionShapeId,
                                 baseVisualShapeIndex=visualShapeId,
                                 basePosition=position)
    return objectId

def create_random_objects(num_objects):
    objects = []
    for _ in range(num_objects):
        x = random.uniform(-0.3, 0.3)
        y = random.uniform(-0.3, 0.3)
        z = 0.8  # Slightly above the table
        objects.append(create_random_object([x, y, z]))
    return objects

# Create objects
objects = create_random_objects(10)

# Set up bird's eye view camera
camera_distance = 1.5
camera_yaw = 0
camera_pitch = -60.9  # Almost looking straight down
camera_target_position = [0, 0, 0.6]  # Focus on the center of the table

p.resetDebugVisualizerCamera(camera_distance, camera_yaw, camera_pitch, camera_target_position)

# Run the simulation
for _ in range(1000000):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()