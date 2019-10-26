using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Runtime.InteropServices;
using UnityEngine.Networking;

public class Komachi_bow : MonoBehaviour
{
  // #if UNITY_WEBGL && !UNITY_EDITOR
  // [DllImport("__Internal")]
  // private static extern string InjectionJs(string url, string id);
  // [DllImport("__Internal")]
  [DllImport("__Internal")]
  public static extern string TestJs();
  [DllImport("__Internal")]
  public static extern string TestJs2();
  [DllImport("__Internal")]
  public static extern string ReadAnimationValue();
  // #endif
  GameObject mirai, angleSlider;
  Animator miraiAnimator;
  HumanPose miraiPose;
  HumanPoseHandler handler;
  AngleControl angleControlScript;

  string csvText;
  List<string[]> csvLines;
  enum Muscles : int
  {
    SpineFrontBack,
    SpineLeftRight,
    SpineTwistLeftRight,
    ChestFrontBack,
    ChestLeftRight,
    ChestTwistLeftRight,
    UpperChestFrontBack,
    UpperChestLeftRight,
    UpperChestTwistLeftRight,
    NeckNodDownUp,
    NeckTiltLeftRight,
    NeckTurnLeftRight,
    HeadNodDownUp,
    HeadTiltLeftRight,
    HeadTurnLeftRight,
    LeftEyeDownUp,
    LeftEyeInOut,
    RightEyeDownUp,
    RightEyeInOut,
    JawClose,
    JawLeftRight,
    LeftUpperLegFrontBack,
    LeftUpperLegInOut,
    LeftUpperLegTwistInOut,
    LeftLowerLegStretch,
    LeftLowerLegTwistInOut,
    LeftFootUpDown,
    LeftFootTwistInOut,
    LeftToesUpDown,
    RightUpperLegFrontBack,
    RightUpperLegInOut,
    RightUpperLegTwistInOut,
    RightLowerLegStretch,
    RightLowerLegTwistInOut,
    RightFootUpDown,
    RightFootTwistInOut,
    RightToesUpDown,
    LeftShoulderDownUp,
    LeftShoulderFrontBack,
    LeftArmDownUp,
    LeftArmFrontBack,
    LeftArmTwistInOut,
    LeftForearmStretch,
    LeftForearmTwistInOut,
    LeftHandDownUp,
    LeftHandInOut,
    RightShoulderDownUp,
    RightShoulderFrontBack,
    RightArmDownUp,
    RightArmFrontBack,
    RightArmTwistInOut,
    RightForearmStretch,
    RightForearmTwistInOut,
    RightHandDownUp,
    RightHandInOut,
    LeftThumb1Stretched,
    LeftThumbSpread,
    LeftThumb2Stretched,
    LeftThumb3Stretched,
    LeftIndex1Stretched,
    LeftIndexSpread,
    LeftIndex2Stretched,
    LeftIndex3Stretched,
    LeftMiddle1Stretched,
    LeftMiddleSpread,
    LeftMiddle2Stretched,
    LeftMiddle3Stretched,
    LeftRing1Stretched,
    LeftRingSpread,
    LeftRing2Stretched,
    LeftRing3Stretched,
    LeftLittle1Stretched,
    LeftLittleSpread,
    LeftLittle2Stretched,
    LeftLittle3Stretched,
    RightThumb1Stretched,
    RightThumbSpread,
    RightThumb2Stretched,
    RightThumb3Stretched,
    RightIndex1Stretched,
    RightIndexSpread,
    RightIndex2Stretched,
    RightIndex3Stretched,
    RightMiddle1Stretched,
    RightMiddleSpread,
    RightMiddle2Stretched,
    RightMiddle3Stretched,
    RightRing1Stretched,
    RightRingSpread,
    RightRing2Stretched,
    RightRing3Stretched,
    RightLittle1Stretched,
    RightLittleSpread,
    RightLittle2Stretched,
    RightLittle3Stretched
  }
  private Animator anim;
  public Slider slider;   //Assign the UI slider of your scene in this slot 

  Animator m_Animator;
  string m_ClipName;
  AnimatorClipInfo[] m_CurrentClipInfo;
  float m_CurrentClipLength;
  float timer;
  [SerializeField]
  private float huga = 0;


  // Use this for initialization
  void Start()
  {
    mirai = GameObject.Find("mirai2019_dance");
    miraiAnimator = mirai.GetComponent<Animator>();
    handler = new HumanPoseHandler(miraiAnimator.avatar, miraiAnimator.transform);
    handler.GetHumanPose(ref miraiPose);
    initZeroPose();
    initUpRightPose();
    //musclesStatus();

    angleSlider = GameObject.Find("Slider");
    angleControlScript = angleSlider.GetComponent<AngleControl>();

    anim = GetComponent<Animator>();
    //Get them_Animator, which you attach to the GameObject you intend to animate.
    m_Animator = gameObject.GetComponent<Animator>();
    //Fetch the current Animation clip information for the base layer
    m_CurrentClipInfo = this.m_Animator.GetCurrentAnimatorClipInfo(0);
    //Access the current length of the clip
    m_CurrentClipLength = m_CurrentClipInfo[0].clip.length;
    //Access the Animation clip name
    m_ClipName = m_CurrentClipInfo[0].clip.name;
    //print(m_CurrentClipLength);
    timer = (1 / m_CurrentClipLength) / 60;
    StartCoroutine(GetText("https://www.e-stat.go.jp/stat-search/file-download?statInfId=000031524010&fileKind=1"));
    ReadCsv(csvText);
  }

  // Update is called once per frame
  void Update()
  {
    // musclesStatus ();
    // getSliderValue();
    moveAnimationBySlider();
    // string rcv_data = TestJsInCs();
    // string rcv_data = ReadAnimationValue();
    // moveAnimationByText(rcv_data);
  }

  private void moveAnimationByText(string data)
  {
    handler.SetHumanPose(ref miraiPose);
    // anim.Play("Komachi_bow_3", 0, 0.147f + 0.343f * huga);
    anim.Play("Komachi_bow_3", 0, 0.147f + 0.343f * float.Parse(data));
    // huga += timer;
  }

  private void moveAnimationBySlider()
  {
    float sliderValue = angleControlScript.getAngleSliderNormalizedValue() * 90 / 146;
    handler.SetHumanPose(ref miraiPose);
    anim.Play("Komachi_bow", 0, sliderValue);
    // sliderValue += timer;
  }

  private void initZeroPose()
  {
    for (int i = 0; i < HumanTrait.MuscleCount; i++)
    {
      miraiPose.muscles[i] = 0f;
    }
    handler.SetHumanPose(ref miraiPose);
  }

  private void initUpRightPose()
  {
    miraiPose.muscles[(int)Muscles.LeftArmDownUp] = -0.6f;
    miraiPose.muscles[(int)Muscles.LeftArmTwistInOut] = 0.15f;
    miraiPose.muscles[(int)Muscles.LeftForearmStretch] = 1f;
    miraiPose.muscles[(int)Muscles.LeftLowerLegStretch] = 0.88f;
    miraiPose.muscles[(int)Muscles.LeftUpperLegFrontBack] = 0.5f;
    miraiPose.muscles[(int)Muscles.RightArmDownUp] = -0.6f;
    miraiPose.muscles[(int)Muscles.RightArmTwistInOut] = 0.15f;
    miraiPose.muscles[(int)Muscles.RightForearmStretch] = 1f;
    miraiPose.muscles[(int)Muscles.RightLowerLegStretch] = 0.88f;
    miraiPose.muscles[(int)Muscles.RightUpperLegFrontBack] = 0.5f;
    miraiPose.muscles[(int)Muscles.SpineFrontBack] = 0f;
    handler.SetHumanPose(ref miraiPose);
  }

  private void musclesStatus()
  {
    string[] muscleName = HumanTrait.MuscleName;
    int i = 0;
    while (i < HumanTrait.MuscleCount)
    {
      //   switch (i)
      //   {
      //     case (int)Muscles.LeftArmDownUp:
      //     case (int)Muscles.LeftArmTwistInOut:
      //     case (int)Muscles.LeftForearmStretch:
      //     case (int)Muscles.LeftLowerLegStretch:
      //     case (int)Muscles.LeftUpperLegFrontBack:
      //     case (int)Muscles.RightArmDownUp:
      //     case (int)Muscles.RightArmTwistInOut:
      //     case (int)Muscles.RightForearmStretch:
      //     case (int)Muscles.RightLowerLegStretch:
      //     case (int)Muscles.RightUpperLegFrontBack:
      //     case (int)Muscles.SpineFrontBack:
      //       Debug.Log((Muscles)System.Enum.ToObject(typeof(Muscles), i) + ":" + muscleName[i] + ":" + miraiPose.muscles[i]);
      //       break;
      //   }
      Debug.Log((Muscles)System.Enum.ToObject(typeof(Muscles), i) + ":" + muscleName[i] + ":" + miraiPose.muscles[i]);
      i++;
    }
  }

  private void getSliderValue()
  {
    float sliderValue = angleControlScript.getAngleSliderNormalizedValue();
    // [parameters of bow_3]
    // 21 Left  Upper Leg Front-Back  :  [0.5 ~ 0.0]
    // 29 Right Upper Leg Front-Back  :  [0.5 ~ 0.0]
    // 0  Spine Front-Back            :  [0.0 ~ -0.5]
    // ?  Root Q.x                    :  [0.0 ~ 0.3]
    miraiPose.muscles[(int)Muscles.LeftUpperLegFrontBack] = 0.5f - 0.5f * sliderValue;
    miraiPose.muscles[(int)Muscles.RightUpperLegFrontBack] = 0.5f - 0.5f * sliderValue;
    miraiPose.muscles[(int)Muscles.SpineFrontBack] = 0.0f - 0.5f * sliderValue;

    float rot = 130 * (0.0f + 0.3f * sliderValue);
    miraiAnimator.transform.RotateAround(new Vector3(0, 0.8f, 0), new Vector3(1, 0, 0), rot - miraiAnimator.transform.rotation.eulerAngles.x);
  }

  private string TestJsInCs()
  {
    return TestJs();
  }

  IEnumerator GetText(string url)
  {
    using (UnityWebRequest www = UnityWebRequest.Get(url))
    {
      yield return www.SendWebRequest();

      if (www.isNetworkError || www.isHttpError)
      {
        Debug.Log(www.error);
      }
      else
      {
        csvText = www.downloadHandler.text;
        // Show results as text
        Debug.Log(csvText);
      }
    }
  }

  List<string[]> ReadCsv(string text)
  {
    string[] csvLine;
    List<string[]> csvLines = new List<string[]>();

    string[] textLines = text.Split('\n');
    for (int i=0;i<textLines.Length;i++)
    {
      csvLine = textLines[i].Split();
      csvLines.Add(csvLine);
      //Debug.Log(csvLine);
    }
    for (int i=0;i<csvLines.Count;i++){
      Debug.Log(csvLines[i]);
    }
    return csvLines;
    
  }

}