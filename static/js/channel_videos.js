  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, {});
  });
var instance = M.Tabs.init(document.getElementById('tab'), {});

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, {hover:false});
  });

  function expandSearch() {
    document.getElementById("search").style.display = "block";
    document.getElementById("search").focus();
}

function hideSearch() {
    document.getElementById("search").style.display = "none";
}
