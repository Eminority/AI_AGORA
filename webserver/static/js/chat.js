// 📌 static/js/chat.js

// 채팅창에 메시지를 추가하는 함수
function addMessageToChat(sender, timestamp, message) {
    let chatBox = document.getElementById("chat-box");
    if (!chatBox) {
        console.error("chat-box 요소를 찾을 수 없습니다.");
        return;
    }
    const pos_name = document.getElementById("pos_name");
    const neg_name = document.getElementById("neg_name");

    timestamp = timestamp.slice(0, 16).replace("T", " ");
    const chat_div = document.createElement("div");
    chat_div.setAttribute("class", `media border p-3`);

    const sender_div = document.createElement("div");
    const sender_span = document.createElement("h4");
    
    const position = document.createElement("div");
    position.innerHTML = sender;

    const timestamp_view = document.createElement("div")
    timestamp_view.innerHTML = timestamp;
    
    
    const chat_body = document.createElement("div");
    chat_body.setAttribute("class", `media-body`);
    const chat_message = document.createElement("div");
    chat_message.innerHTML = message;


    const avatar = document.createElement("img");
    avatar.setAttribute("class", "mr-3 mt-3 rounded-circle");
    avatar.setAttribute("style", "width:60px; height:60px;");

    if (sender == "pos"){
        //pos측이면 이름-시간-내용
        sender_span.innerHTML = pos_name.getAttribute("data-name");
        sender_div.appendChild(sender_span);
        sender_div.appendChild(timestamp_view);
        sender_div.appendChild(position);
        
        avatar.setAttribute("src", pos_name.getAttribute("data-imgpath"));
        sender_div.appendChild(avatar);

        chat_body.appendChild(chat_message);
        chat_div.appendChild(sender_div);
        chat_div.appendChild(chat_body);
    } else if (sender == "neg"){
        //neg측이면 내용-시간-이름
        sender_span.innerHTML = neg_name.getAttribute("data-name");
        sender_span.setAttribute("class", "text-right");
        sender_div.appendChild(sender_span);
        timestamp_view.setAttribute("class", "text-right");
        sender_div.appendChild(timestamp_view);
        position.setAttribute("class", "text-right");
        sender_div.appendChild(position);
        
        avatar.setAttribute("src", neg_name.getAttribute("data-imgpath"));
        sender_div.setAttribute("class","text-right");
        sender_div.appendChild(avatar);
        
        chat_body.appendChild(chat_message);
        chat_div.appendChild(chat_body);
        chat_div.appendChild(sender_div);
    } else {
        //judge면 가운데
        sender_div.setAttribute("class","text-center");
        const judgeposition = document.createElement("h4");
        judgeposition.setAttribute("class", "text-center");
        judgeposition.innerHTML = sender;
        sender_div.appendChild(judgeposition);
        sender_div.appendChild(timestamp_view);
        
        chat_body.appendChild(sender_div);
        chat_message.setAttribute("class","text-center");
        chat_div.setAttribute("class", "media border p-3 bg-light")
        chat_body.appendChild(chat_message);
        chat_div.appendChild(chat_body);
    }
    
    chatBox.appendChild(chat_div);

    // 📌 채팅창 자동 스크롤 (새로운 메시지가 보이도록)
    chatBox.scrollTop = chatBox.scrollHeight;
}
