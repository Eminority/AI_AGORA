document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("yoloDetectForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const fileInput = document.getElementById("original_image");
        if (!fileInput.files.length) {
            alert("파일을 선택하세요.");
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        // 서버에 이미지 업로드 요청
        const response = await fetch(document.getElementById("yoloDetectForm").getAttribute("data-object-detect-url"), {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log("서버 응답:", result);

        // 서버에서 받은 list 데이터를 기반으로 radio 버튼 생성
        generateRadioButtons(result.object);

        if (result.result){
            document.getElementById("generateAI_area").style.display = "block";
        }
    });

    function generateRadioButtons(options) {
        const container = document.getElementById("detected-list");
        container.innerHTML = "";  // 기존 내용 초기화
        console.log(options)
        if (!options.length) {
            container.innerHTML = "<p>감지된 객체가 없습니다.</p>";
            return;
        }

        options.forEach((option, index) => {
            const label = document.createElement("label");
            label.innerHTML = `
                <input type="radio" name="name" value="${option} required" ${index === 0 ? "checked" : ""}>
                ${option}
            `;
            container.appendChild(label);
            container.appendChild(document.createElement("br"));  // 줄바꿈
        });
    }


    //submit 시 새로고침 방지
    document.getElementById("ImageSelectedForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const selectedObject = document.querySelector('input[name="selected-object"]:checked');

        if (!selectedObject) {
            alert("객체를 선택하세요.");
            return;
        }

        const formData = new FormData();
        formData.append("selected_object", selectedObject.value);

        // FastAPI 서버에 선택한 객체 정보 전송
        const response = await fetch("{{ request.url_for('create_profile') }}", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log("선택한 객체:", result);

        alert(`선택한 객체: ${result.selected}`);
    });
})