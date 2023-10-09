function validateForm() {
    var select = document.getElementById('selectOption');
    var submitButton = document.getElementById('submitButton');

    // オプションが選択されているかを確認
    if (select.value === '駅検索...') {
        alert('オプションを選択してください。');
        return false; // 送信を中止
    }

    return true; // フォームを送信
}




// カード要素を取得
var cards = document.querySelectorAll(".card");

// カードをクリックしたときのアクションを設定
cards.forEach(function(card, index) {
    card.addEventListener("click", function() {
        var cardId = this.getAttribute("data-card-id");
        var cardName = this.querySelector(".card-title").textContent;

        // クリックしたカードの情報を取得
        var cardInfo = {
            id: cardId,
            name: cardName
        };

        // カード情報をJSON文字列に変換
        var cardInfoJson = JSON.stringify(cardInfo);

        // フォームを作成してカード情報を送信
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/rent_info";

        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "card_info";
        input.value = cardInfoJson;

        form.appendChild(input);
        document.body.appendChild(form);

        // フォームを送信
        form.submit();
    });
});



document.addEventListener("DOMContentLoaded", function() {
    var geoInfoButton = document.getElementById("geoinfo-link");
    
    geoInfoButton.addEventListener("click", function() {
        var parentElement = geoInfoButton.closest(".parent-element");
        var tenaid = parentElement.dataset.tenaId;

        console.log(tenaid);

        // フォームを作成してカード情報を送信
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/GeoInfo";
    
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "card_info";
        input.value = tenaid; // JSON.stringifyを使用せずに直接値を代入
        
        form.appendChild(input);
        document.body.appendChild(form);
    
        // フォームを送信
        form.submit();
    });
});



document.addEventListener("DOMContentLoaded", function() {
    var geoInfoButton = document.getElementById("calc-link");
    
    geoInfoButton.addEventListener("click", function() {
        var parentElement = geoInfoButton.closest(".parent-element");
        var tenaid = parentElement.dataset.tenaId;

        console.log(tenaid);

        // フォームを作成してカード情報を送信
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/calc";
    
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "card_info";
        input.value = tenaid; // JSON.stringifyを使用せずに直接値を代入
        
        form.appendChild(input);
        document.body.appendChild(form);
    
        // フォームを送信
        form.submit();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var geoInfoButton = document.getElementById("basicinfo-link");
    
    geoInfoButton.addEventListener("click", function() {
        var parentElement = geoInfoButton.closest(".parent-element");
        var tenaid = parentElement.dataset.tenaId;

        console.log(tenaid);

        // フォームを作成してカード情報を送信
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/rent_info";
    
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "card_info";
        input.value = tenaid; // JSON.stringifyを使用せずに直接値を代入
        
        form.appendChild(input);
        document.body.appendChild(form);
    
        // フォームを送信
        form.submit();
    });
});
