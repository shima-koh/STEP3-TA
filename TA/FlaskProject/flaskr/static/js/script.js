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

cards.forEach(function(card) {
    card.addEventListener("click", function() {
        var cardId = this.getAttribute("data-card-id");
        
        // カードIDをフォームに設定
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/rent_info";
        
        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "card_id";
        input.value = cardId;
        
        form.appendChild(input);
        document.body.appendChild(form);
        
        // フォームを送信
        form.submit();
    })
});


