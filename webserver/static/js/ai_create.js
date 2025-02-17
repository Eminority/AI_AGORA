document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("yoloDetectForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const fileInput = document.getElementById("original_image");
        if (!fileInput.files.length) {
            alert("파일을 선택하세요.");
            return;
        }

        const formData = new FormData();
        formData.append("original_image", fileInput.files[0]);

        // 서버에 이미지 업로드 요청
        const yoloDetectFormRequestURL = document.getElementById("yoloDetectForm").getAttribute("data-object-detect-url");
        const response = await fetch(yoloDetectFormRequestURL, {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log("서버 응답:", result);

        // 서버에서 받은 list 데이터를 기반으로 radio 버튼 생성
        if (result.result == true){
            generateRadioButtons(result.data);
            document.getElementById("generateAI_area").style = "display: block;";
        }
    });

    function generateRadioButtons(options) {
        const container = document.getElementById("detected-list");
        container.innerHTML = "";  // 기존 내용 초기화
        let options_len = 0;
        Object.entries(options).forEach(([key, data], index) => {
            const label = document.createElement("label");
            label.innerHTML = `
                <input type="radio" name="name" value="${data.name}" data-filename="${key}" required ${index === 0 ? "checked" : ""}>
                ${data.name}
            `;
            container.appendChild(label);
            container.appendChild(document.createElement("br"));  // 줄바꿈
            options_len++;
        });
        if (options_len == 0){
            alert(`감지된 물체가 없습니다.`);
            container.innerHTML = `<p>감지된 물체 없음</p>`
            const text_to_profile_object = document.createElement("div");
            text_to_profile_object.innerHTML = `
                <label for="name">객체가 무엇인지 직접 입력해주세요.</label>
                <input type="text" class="form-control" id="name" name="name" placeholder="cat"/>
            `;
            container.appendChild(text_to_profile_object)
        }
    }


    //submit 시 새로고침 방지
    document.getElementById("ImageSelectedForm").addEventListener("submit", async function (event) {
        event.preventDefault();
        let selectedObject = document.querySelector('input[name="name"]:checked');
        const selectedAI = document.getElementById('ai');
        if (!selectedObject){
            selectedObject = document.getElementById("name");
        }
        if (!selectedObject.value) {
            alert("객체를 선택하세요.");
            return;
        }

        const formData = new FormData();
        const filepath = selectedObject.getAttribute("data-filename");
        formData.append("selected_object", selectedObject.value);
        formData.append("file_path", filepath?filepath:"DEFAULT");
        formData.append("ai", selectedAI.value);
        // FastAPI 서버에 선택한 객체 정보 전송
        const createProfileRequestURL =  document.getElementById("ImageSelectedForm").getAttribute("data-create-profile-url");
        const response = await fetch(createProfileRequestURL, {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log("선택한 객체:", result);
        if (result.result === "success"){
            alert(`선택한 객체 ${selectedObject.value} 로 AI가 생성중입니다...`);
        }
    });
})