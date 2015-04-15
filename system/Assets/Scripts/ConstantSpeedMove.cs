using UnityEngine;
using System.Collections;

public class ConstantSpeedMove : MonoBehaviour {

	public Vector3 s0;
	public Vector3 v0;

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
		gameObject.transform.position = s0 + v0 * Time.time;
	}
}
