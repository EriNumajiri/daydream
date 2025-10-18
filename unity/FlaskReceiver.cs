using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class FlaskReceiver : MonoBehaviour
{
    // 🔹 Renderでデプロイした Flask のURL（https://◯◯.onrender.com）
    public string serverUrl = "https://daydream-c1bk.onrender.com";

    void Start()
    {
        // 定期的にFlaskへping（5分おき）
        InvokeRepeating(nameof(SendPing), 0f, 300f);

        // 最初にデータを受け取る
        StartCoroutine(GetAnswers());
    }

    IEnumerator SendPing()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + "/ping");
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("✅ FlaskにPing成功：" + www.downloadHandler.text);
        }
        else
        {
            Debug.LogWarning("⚠️ Ping失敗: " + www.error);
        }
    }

    IEnumerator GetAnswers()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + "/get-answers");
        yield return www.SendWebRequest();

        if (www.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("📩 Flaskから受け取ったデータ:");
            Debug.Log(www.downloadHandler.text);
            // ここでJSONを解析して使うこともできる！
        }
        else
        {
            Debug.LogError("データ取得失敗: " + www.error);
        }
    }
}
