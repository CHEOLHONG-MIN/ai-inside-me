// 요약문 복사 시 사용자 알림 개선
function copySummary() {
  const text = document.getElementById("summaryText").innerText;
  navigator.clipboard.writeText(text);
  const btn = document.getElementById("copyBtn");
  btn.innerText = "✅ 복사됨!";
  setTimeout(() => btn.innerText = "복사하기", 1500);
}
