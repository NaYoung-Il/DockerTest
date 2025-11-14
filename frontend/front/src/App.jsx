import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("이미지를 선택하세요!");
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://localhost:8000/predict/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    setResult(res.data);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>이미지 분류</h1>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => {
          setFile(e.target.files[0]);
          setPreview(URL.createObjectURL(e.target.files[0]));
        }}
      />
      <button onClick={handleUpload} style={{ marginLeft: "10px" }}>
        업로드
      </button>

      {preview && (
        <div style={{ marginTop: "20px" }}>
          <img src={preview} alt="preview" width="300px" />
        </div>
      )}

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>결과: {result.label}</h2>
          <p>신뢰도: {(result.con_score * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}

export default App;