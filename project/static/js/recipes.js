import '../scss/recipes.scss';


window.addEventListener('DOMContentLoaded', () => {
    // 初期化処理（こちらの方が早いかも）
    initPage();
})

// 初期化処理
const initPage = ()=> {
    var input_title = document.getElementById('inputed-title');
    var input_categorys = document.getElementById('inputed-categorys');
    var input_materials = document.getElementById('inputed-materials');

    if (input_title !== null) {
        document.getElementById('title-recipe').value = input_title.textContent;
    }
    if (input_categorys !== null) {
        var category_item_list = document.querySelectorAll('#category-recipe option');
        category_item_list.forEach((data)=> {
            if (data.value === input_categorys.textContent) {
                data.selected = true;
            }
        })
    }
    if (input_materials !== null) {
        var material_item_list = document.querySelectorAll('#material-check-box .material-item');
        var checked_item_list = input_materials.textContent.split(",");
        material_item_list.forEach((data)=> {
            checked_item_list.forEach((item)=>{
                if(parseInt(item) === parseInt(data.value)) {
                    data.checked = true;
                }
            })
        })
    }
}


let form_button = document.querySelector(".search-button");

form_button.onclick = () => {
    let form = document.querySelector("#search-recipe-form");
    form.title.value = document.querySelector(".search-form-ara #title-recipe").value;

    const select_category = document.querySelector("#category-recipe");
    form.categorys.value = select_category.value;

    const checkbox_material = document.querySelectorAll('#material-check-box .material-item');
    
    let result_material = [];
    checkbox_material.forEach((material)=> {
        if (material.checked){
            result_material.push(material.value);
        }
    })
    form.materials.value = result_material;
    form.submit();
}



let recipe_article = document.querySelectorAll(".recipe-article");

recipe_article.forEach((article) => {
    article.addEventListener('click', () => {
        let children = article.children;
        Array.prototype.forEach.call(children, function (item) {
          if (item.tagName == "A") {
              console.log('href : ' + item.getAttribute("href"));
              window.location.href = item.getAttribute("href");
          }
        });
    }, true);
})
