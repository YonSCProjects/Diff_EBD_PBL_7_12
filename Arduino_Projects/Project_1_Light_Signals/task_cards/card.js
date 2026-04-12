/* card.js — interactive checkbox persistence for Hebrew navigation cards.
 *
 * Screen-only behaviour (hidden under @media print). On first load the
 * student is asked for their nickname (matching the Cheetah/Fox/etc.
 * convention already used for their Google Drive folder). Checklist
 * state is then persisted in localStorage keyed by
 *   "<nickname>::<card-id>::<item-index>"
 * so the same shared workstation remembers each student's progress
 * independently. A small header strip shows the current nickname with
 * two buttons: switch-nickname and reset-this-card.
 *
 * Loaded by Hebrew task cards via <script src="../task_cards/card.js"></script>.
 */
(function () {
  'use strict';

  var NICKNAME_KEY = 'agourim_card_nickname';

  function getNickname() {
    return localStorage.getItem(NICKNAME_KEY);
  }

  function askForNickname() {
    var current = getNickname() || '';
    var input = window.prompt('מה הכינוי שלך? (לדוגמה: Cheetah)', current);
    if (input === null) return null;
    var trimmed = input.trim();
    if (!trimmed) return null;
    localStorage.setItem(NICKNAME_KEY, trimmed);
    return trimmed;
  }

  function getCardId(card) {
    var badge = card.querySelector('.card-id');
    if (!badge) return 'unknown-card';
    return badge.textContent.trim().replace(/\s+/g, '-');
  }

  function storageKey(nickname, cardId, idx) {
    return nickname + '::' + cardId + '::' + idx;
  }

  function buildIndicator(nickname, onSwitch, onReset) {
    var bar = document.createElement('div');
    bar.className = 'nickname-indicator';
    bar.setAttribute('dir', 'rtl');

    var label = document.createElement('span');
    label.innerHTML = 'כינוי: <strong></strong>';
    label.querySelector('strong').textContent = nickname;
    bar.appendChild(label);

    var switchBtn = document.createElement('button');
    switchBtn.type = 'button';
    switchBtn.textContent = 'החלף כינוי';
    switchBtn.addEventListener('click', onSwitch);
    bar.appendChild(switchBtn);

    var resetBtn = document.createElement('button');
    resetBtn.type = 'button';
    resetBtn.textContent = 'איפוס סימונים';
    resetBtn.addEventListener('click', onReset);
    bar.appendChild(resetBtn);

    return bar;
  }

  function initCard() {
    var card = document.querySelector('.card');
    if (!card) return;
    var checklistItems = card.querySelectorAll('.checklist li');
    if (checklistItems.length === 0) return;

    var nickname = getNickname();
    if (!nickname) {
      nickname = askForNickname();
      if (!nickname) return;
    }

    var cardId = getCardId(card);

    function applyStoredState() {
      checklistItems.forEach(function (li, idx) {
        var key = storageKey(nickname, cardId, idx);
        if (localStorage.getItem(key) === '1') {
          li.classList.add('checked');
        } else {
          li.classList.remove('checked');
        }
      });
    }

    function onSwitch() {
      var newName = askForNickname();
      if (!newName) return;
      nickname = newName;
      indicator.querySelector('strong').textContent = nickname;
      applyStoredState();
    }

    function onReset() {
      if (!window.confirm('לאפס את הסימונים שלך בכרטיסייה הזאת?')) return;
      checklistItems.forEach(function (li, idx) {
        localStorage.removeItem(storageKey(nickname, cardId, idx));
        li.classList.remove('checked');
      });
    }

    var indicator = buildIndicator(nickname, onSwitch, onReset);
    card.insertBefore(indicator, card.firstChild);

    applyStoredState();

    checklistItems.forEach(function (li, idx) {
      li.addEventListener('click', function () {
        var key = storageKey(nickname, cardId, idx);
        var nowChecked = li.classList.toggle('checked');
        if (nowChecked) {
          localStorage.setItem(key, '1');
        } else {
          localStorage.removeItem(key);
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCard);
  } else {
    initCard();
  }
})();
