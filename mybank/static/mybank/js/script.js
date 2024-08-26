// Scripts implemented on dashboard.html

/**
 * Two separated functions that serves the similar purpose. One for desktop sidebar and the other for mobile bottom navbar
 * Sets the active state for dashboard buttons by adding the 'active-btn'/'active-btn-2' classes
 * to the clicked button and removing it from all other buttons with the 'custom-nav-btn'/'custom-nav-btn-2 class.
 * These functions ensure that only one button is highlighted at a time in the sidebar navigation or bottom navbar
 */
function setActive(element) {
    var links = document.querySelectorAll('.custom-nav-btn');

    links.forEach(function(link) {
        link.classList.remove('active-btn');
    });

    element.classList.add('active-btn');
}

function setActive2(element) {
    var links = document.querySelectorAll('.custom-nav-btn-2');

    links.forEach(function(link) {
        link.classList.remove('active-btn-2');
    });

    element.classList.add('active-btn-2');
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.custom-nav-btn').forEach(link => {
        link.addEventListener('click', function() {
            setActive(this);
        });
    });

    const currentPath = window.location.pathname;
    document.querySelectorAll('.custom-nav-btn').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            setActive(link);
        }
    });

    document.querySelectorAll('.custom-nav-btn-2').forEach(link => {
        link.addEventListener('click', function() {
            setActive2(this);
        });
    });

    document.querySelectorAll('.custom-nav-btn-2').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            setActive2(link);
        }
    });
    
});

// #TODO Make top navigation script too
// Transaction History Filter functionality
// #TODO The script is inside the transaction_history.html, script was not working on a separate File, debugging is much needed

// #TODO: COOKIE CONSENT BANNER


// #TODO: For enhancements, interpolation of dashboard views to javascript charts should be implemented
document.addEventListener('DOMContentLoaded', function() {
    // Dummy Data for frontend demonstration purpose only. Uses Chart.js library to render a chart
      var ctx = document.getElementById('balanceChart').getContext('2d');

      var accountBalance = 'Account Balance: $100,000';

      var balanceChart = new Chart(ctx, {
          type: 'line', 
          data: {
              labels: ['May', 'June', 'July', 'August', 'September', 'October'], 
              datasets: [{
                  label: accountBalance,
                  data: [1200, 1500, 1400, 1600, 1550, 1700],
                  borderColor: 'rgba(75, 192, 192, 1)', 
                  backgroundColor: 'rgba(75, 192, 192, 0.2)', 
                  borderWidth: 2
              }]
          },
          options: {
              responsive: true,
              plugins: {
                  legend: {
                      display: true,
                      labels: {
                          font: {
                              size: 18
                          }
                      }
                  }
              },
              scales: {
                  x: {
                      beginAtZero: true
                  },
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });

  });

/**
 * Fetches stock data from Finnhub API and updates the stock table.
 * Displays current, high, low, open, and previous close prices for a list of stock symbols.
 * Public key is deleted security purposes
 */
  const apiKey = '';
        const symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'];
        const url = symbol => `https://finnhub.io/api/v1/quote?symbol=${symbol}&token=${apiKey}`;

        async function fetchStockData(symbols) {
            const fetchPromises = symbols.map(symbol => fetch(url(symbol)).then(res => res.json()));
            return Promise.all(fetchPromises);
        }

        function createTableRows(stockData, symbols) {
            return stockData.map((data, index) => {
                return `
                    <tr>
                        <td>${symbols[index]}</td>
                        <td>$${data.c.toFixed(2)}</td> <!-- Current Price -->
                        <td>$${data.h.toFixed(2)}</td> <!-- High Price -->
                        <td>$${data.l.toFixed(2)}</td> <!-- Low Price -->
                        <td>$${data.o.toFixed(2)}</td> <!-- Open Price -->
                        <td>$${data.pc.toFixed(2)}</td> <!-- Previous Close -->
                    </tr>
                `;
            }).join('');
        }

        document.addEventListener('DOMContentLoaded', async function() {
            const stockDataArray = await fetchStockData(symbols);
            const tableBody = document.querySelector('#stockTable tbody');
            tableBody.innerHTML = createTableRows(stockDataArray, symbols);
        });
