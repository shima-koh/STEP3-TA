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
        var tenaid = this.getAttribute("data-card-id");

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


//GeoInfo Button
document.addEventListener("DOMContentLoaded", function() {
    var geoInfoButton = document.getElementById("geoinfo-link");
    
    geoInfoButton.addEventListener("click", function() {
        var parentElement = geoInfoButton.closest(".parent-element");
        var tenaid = parentElement.dataset.tenaId;

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


//Calc Button
document.addEventListener("DOMContentLoaded", function() {
    var calcButton = document.getElementById("calc-link");
    
    calcButton.addEventListener("click", function() {
        var parentElement = calcButton.closest(".parent-element");
        var tenaid = parentElement.dataset.tenaId;

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

//BasicInfo Button
document.addEventListener("DOMContentLoaded", function() {
    var basicInfoButton = document.getElementById("basicinfo-link");
    
    basicInfoButton.addEventListener("click", function() {
        var parentElement = basicInfoButton.closest(".parent-element");
        var tenaid = parentElement.dataset.tenaId;


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

//HOmeへ遷移
// buttonをクリックしたときのアクションを設定
var homeButton = document.getElementById("home-link");

// ボタンがクリックされたときの処理
homebutton.addEventListener("click", function() {
  // ページ遷移
    window.location.href = "/";
});


