/**
 * JobTrack Pro - Interactive UI & Client Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initKanbanDragAndDrop();
  initTableStatusUpdates();
  initViewSwitcher();
  initKeyboardShortcuts();
});

/**
 * Theme Toggle Handler
 */
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');
  const storedTheme = localStorage.getItem('careerpulse_theme') || 'dark';

  document.documentElement.setAttribute('data-theme', storedTheme);
  updateThemeIcon(storedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('careerpulse_theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }

  function updateThemeIcon(theme) {
    if (!themeIcon) return;
    if (theme === 'light') {
      themeIcon.className = 'bi bi-moon-stars-fill';
      themeToggleBtn.setAttribute('title', 'Switch to Dark Mode');
    } else {
      themeIcon.className = 'bi bi-sun-fill text-warning';
      themeToggleBtn.setAttribute('title', 'Switch to Light Mode');
    }
  }
}

/**
 * Kanban Drag and Drop with AJAX Status Updates
 */
function initKanbanDragAndDrop() {
  const cards = document.querySelectorAll('.kanban-card');
  const columns = document.querySelectorAll('.kanban-column-body');

  cards.forEach(card => {
    card.addEventListener('dragstart', (e) => {
      card.classList.add('dragging');
      e.dataTransfer.setData('text/plain', card.getAttribute('data-id'));
      e.dataTransfer.effectAllowed = 'move';
    });

    card.addEventListener('dragend', () => {
      card.classList.remove('dragging');
    });
  });

  columns.forEach(column => {
    column.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      column.classList.add('drag-over');
    });

    column.addEventListener('dragleave', () => {
      column.classList.remove('drag-over');
    });

    column.addEventListener('drop', async (e) => {
      e.preventDefault();
      column.classList.remove('drag-over');

      const applicationId = e.dataTransfer.getData('text/plain');
      const targetStatus = column.getAttribute('data-status');
      const draggedCard = document.querySelector(`.kanban-card[data-id="${applicationId}"]`);

      if (!draggedCard || !targetStatus) return;

      const currentStatus = draggedCard.getAttribute('data-current-status');
      if (currentStatus === targetStatus) return;

      // Optimistically move card
      column.appendChild(draggedCard);
      draggedCard.setAttribute('data-current-status', targetStatus);

      // Update counters in headers
      updateColumnCounters();

      // Submit AJAX update to backend
      try {
        const csrfToken = getCsrfToken();
        const response = await fetch(`/application/${applicationId}/status/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
          },
          body: new URLSearchParams({ 'status': targetStatus })
        });

        const data = await response.json();
        if (data.success) {
          showFloatingToast(`Moved to ${data.status_label}`, 'success');
        } else {
          showFloatingToast('Could not update status: ' + (data.error || 'Server error'), 'danger');
        }
      } catch (err) {
        console.error('Error updating status:', err);
        showFloatingToast('Network error while updating status', 'danger');
      }
    });
  });
}

function updateColumnCounters() {
  document.querySelectorAll('.kanban-column').forEach(col => {
    const status = col.getAttribute('data-column-status');
    const count = col.querySelectorAll('.kanban-card').length;
    const badge = col.querySelector('.column-count-badge');
    if (badge) badge.textContent = count;
  });
}

/**
 * Table inline status dropdown changer
 */
function initTableStatusUpdates() {
  const statusSelects = document.querySelectorAll('.table-status-select');
  statusSelects.forEach(select => {
    select.addEventListener('change', async (e) => {
      const appId = select.getAttribute('data-id');
      const newStatus = select.value;
      const csrfToken = getCsrfToken();

      try {
        const response = await fetch(`/application/${appId}/status/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
          },
          body: new URLSearchParams({ 'status': newStatus })
        });

        const data = await response.json();
        if (data.success) {
          showFloatingToast(`Status updated to ${data.status_label}`, 'success');
        } else {
          showFloatingToast('Status update failed', 'danger');
        }
      } catch (err) {
        showFloatingToast('Connection error', 'danger');
      }
    });
  });
}

/**
 * Grid View / Table View Switcher
 */
function initViewSwitcher() {
  const tableViewBtn = document.getElementById('viewTableBtn');
  const gridViewBtn = document.getElementById('viewGridBtn');
  const tableView = document.getElementById('tableViewContainer');
  const gridView = document.getElementById('gridViewContainer');

  if (!tableViewBtn || !gridViewBtn || !tableView || !gridView) return;

  const savedView = localStorage.getItem('jobtrack_view_pref') || 'table';
  applyView(savedView);

  tableViewBtn.addEventListener('click', () => {
    applyView('table');
    localStorage.setItem('jobtrack_view_pref', 'table');
  });

  gridViewBtn.addEventListener('click', () => {
    applyView('grid');
    localStorage.setItem('jobtrack_view_pref', 'grid');
  });

  function applyView(view) {
    if (view === 'grid') {
      tableView.classList.add('d-none');
      gridView.classList.remove('d-none');
      gridViewBtn.classList.add('active');
      tableViewBtn.classList.remove('active');
    } else {
      gridView.classList.add('d-none');
      tableView.classList.remove('d-none');
      tableViewBtn.classList.add('active');
      gridViewBtn.classList.remove('active');
    }
  }
}

/**
 * Keyboard shortcuts
 */
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    const isInput = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName);

    // Ctrl+K or Cmd+K: Focus search
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      const searchInput = document.getElementById('searchInput');
      if (searchInput) searchInput.focus();
    }

    // 'N' to open New Application modal when not in an input
    if (!isInput && (e.key === 'n' || e.key === 'N') && !e.ctrlKey && !e.metaKey) {
      const modalTrigger = document.querySelector('[data-bs-target="#quickAddModal"]');
      if (modalTrigger) {
        e.preventDefault();
        const modal = new bootstrap.Modal(document.getElementById('quickAddModal'));
        modal.show();
      }
    }
  });
}

/**
 * CSRF Token helper
 */
function getCsrfToken() {
  const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
  if (tokenInput) return tokenInput.value;
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  return cookieValue || '';
}

/**
 * Floating Toast notification
 */
function showFloatingToast(message, type = 'primary') {
  let container = document.getElementById('floating-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'floating-toast-container';
    container.style.position = 'fixed';
    container.style.bottom = '24px';
    container.style.right = '24px';
    container.style.zIndex = '9999';
    container.style.display = 'flex';
    container.style.flexDirection = 'column';
    container.style.gap = '10px';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `alert alert-${type} alert-custom d-flex align-items-center shadow-lg py-2 px-3 fade show`;
  toast.style.minWidth = '240px';
  toast.style.margin = '0';
  toast.innerHTML = `
    <i class="bi ${type === 'success' ? 'bi-check-circle-fill text-success' : 'bi-info-circle-fill text-primary'} me-2 fs-5"></i>
    <span class="flex-grow-1">${message}</span>
    <button type="button" class="btn-close ms-2" style="font-size: 0.75rem;" onclick="this.parentElement.remove()"></button>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
