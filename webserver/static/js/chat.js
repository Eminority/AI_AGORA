// 📌 static/js/chat.js

// 채팅창에 메시지를 추가하는 함수
function addMessageToChat(sender, timestamp, message) {
    let chatBox = document.getElementById("chat-box");
    if (!chatBox) {
        console.error("chat-box 요소를 찾을 수 없습니다.");
        return;
    }

    const chat_div = document.createElement("div");
    chat_div.setAttribute("class", `media border p-3`);
    chat_div.innerHTML = `<h4>${sender}</h4> <span>${timestamp}</span>`;
    
    const chat_body = document.createElement("div");
    chat_body.setAttribute("class", `media-body`)
    chat_body.innerHTML = `${message}`

    chat_div.appendChild(chat_body);
    
    chatBox.appendChild(chat_div);

    // 📌 채팅창 자동 스크롤 (새로운 메시지가 보이도록)
    chatBox.scrollTop = chatBox.scrollHeight;
}
