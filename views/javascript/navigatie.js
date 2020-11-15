window.onload = function(){
    var id = document.getElementsByName('active-nav')[0].getAttribute('content');
    document.getElementById(id).className += ' active';
    document.getElementById(id).content += ' <span class="sr-only">(current)</span>';
  }
  
  function navigatie(){
    var id = document.getElementsByName('active-nav')[0].getAttribute('content');
    document.getElementById(id).className += ' active';
    document.getElementById(id).content += ' <span class="sr-only">(current)</span>';
  }
  