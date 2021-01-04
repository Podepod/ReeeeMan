window.onload = function(){
    var id = document.getElementsByName('active-nav')[0].getAttribute('content');
    if(document.getElementById(id).className == 'dropdown-item'){
      console.log("dropdown");
      parentId = document.getElementById(id).parentElement.getAttribute('aria-labelledby')
      document.getElementById(parentId).className += ' active';
      document.getElementById(parentId).content += ' <span class="sr-only">(current)</span>';
    }
    document.getElementById(id).className += ' active';
    document.getElementById(id).content += ' <span class="sr-only">(current)</span>';
  }
  
  function navigatie(){
    var id = document.getElementsByName('active-nav')[0].getAttribute('content');
    if(document.getElementById(id).className == 'dropdown-item'){
      console.log("dropdown");
      parentId = document.getElementById(id).parentElement.getAttribute('aria-labelledby')
      document.getElementById(parentId).className += ' active';
      document.getElementById(parentId).content += ' <span class="sr-only">(current)</span>';
    }    
    document.getElementById(id).className += ' active';
    document.getElementById(id).content += ' <span class="sr-only">(current)</span>';
  }
  