using UnityEngine;  // This script allows the camera to orbit around a target object based on mouse input.

public class CameraOrbit : MonoBehaviour  // This class handles the camera orbiting functionality.
{
    public Transform target;   // The point around which the camera will orbit
    public float rotationSpeed = 5f;  // Speed of rotation
    private Vector3 offset;    // Initial offset from the target

    void Start()  // This method is called when the script instance is being loaded.
    {
        // Check if the target is assigned
        if (target == null)
        {
            Debug.LogError("No target assigned to the camera!");
            return;
        }

        // Set the initial offset based on the target's position
        offset = transform.position - target.position;
    }
    {
        if (target != null)
        {
            // Store the initial offset between camera and target
            offset = transform.position - target.position;
            Debug.Log(offset);
            Debug.Log("Camera set");
        }
        else
{
    Debug.LogError("No target assigned to the camera!");
}
    }

    void Update()
{
    if (target != null)
    {
        // Get user input from mouse movement
        float horizontalInput = Input.GetAxis("Mouse X") * rotationSpeed;
        float verticalInput = Input.GetAxis("Mouse Y") * rotationSpeed;

        // Rotate the offset based on input
        Quaternion rotation = Quaternion.Euler(-verticalInput, horizontalInput, 0);
        offset = rotation * offset;

        // Update the camera position
        transform.position = target.position + offset;

        // Make the camera always look at the target
        transform.LookAt(target);
    }
}
}
