using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.IO;

public class cameraInput : MonoBehaviour
{
    private WebCamTexture textureWebCam = null;

    private int camWidth;
    private int camHeight;
    public string dirPath;
    public GameObject objTarget = null;
    public Button camerButton;

    void Start()
    {
        camWidth = Screen.width;
        camHeight = Screen.height;
        CameraOn();
        if(textureWebCam != null)
        {
            textureWebCam.Play();
        }
    }

    void CameraOn()
    {
        Debug.Log("Start");
        dirPath = Application.dataPath + "/../SaveImages/";

        // 현재 사용 가능한 카메라 리스트
        WebCamDevice[] devices = WebCamTexture.devices;

        // 사용할 카메라 선택
        // 가장 처음 검색되는 후면 카메라 사용
        int selectedCameraIndex = -1;
        for(int i = 0; i < devices.Length; i++)
        {
            Debug.Log("Available Cam : " + devices[i].name + ((devices[i].isFrontFacing) ? "(Front)" : "Back"));

            // 후면 카메라면 해당 카메라 선택
            if (devices[i].isFrontFacing == false)
            {
                selectedCameraIndex = i;
                break;
            }
        }

        // WebCamTexture 생성 
        if(selectedCameraIndex >= 0)
        {
            // 선택된 카메라에 대한 WebCamTexture 생성
            textureWebCam = new WebCamTexture(devices[selectedCameraIndex].name);
            // 원하는 FPS 설정
            if (textureWebCam != null) textureWebCam.requestedFPS = 60;
        }

        // objTarget에 카메라 표시
        if(textureWebCam  != null)
        {
            Renderer render = objTarget.GetComponent<Renderer>();
            render.material.mainTexture = textureWebCam;
        }
    }


    public void OnClick()
    {
        DirectoryInfo dir = new DirectoryInfo(dirPath);
        if (!dir.Exists)
        {
            Directory.CreateDirectory(dirPath);
        }
        string name = "object.png";
        RenderTexture rt = new RenderTexture(camWidth, camHeight, 24);

        Graphics.Blit(textureWebCam, rt);
        Texture2D screenShot = new Texture2D(camWidth, camHeight, TextureFormat.RGB24, false);
        RenderTexture.active = rt;
        screenShot.ReadPixels(new Rect(0, 0, camWidth, camHeight), 0, 0);
        screenShot.Apply();
        byte[] bytes = screenShot.EncodeToPNG();
        File.WriteAllBytes(dirPath + name, bytes);

        textureWebCam.Stop();
    }
}
