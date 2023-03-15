$(document).ready(function () {
    $.ajax({
      url: 'http://localhost:5000/max_transactions',
      type: 'GET',
      success: function (data) {
        let table = `
        <table class="table w-75 table-striped">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Market</th>
              <th scope="col">Amount</th>
              <th scope="col">Price (CLP)</th>
              <th scope="col">Max Transaction (CLP)</th>
              <th scope="col">Buy/Sell</th>
            </tr>
          </thead>
          <tbody>
        `;
        var options = { style: 'currency', currency: 'USD' };
        let idx = 1;
        for (each of data) {
          table += `<tr>`;
          table += `<th scope="row">${idx}</th>`;
          table += `<td>${each['market']}</td>`;
          table += `<td>${each['amount']}</td>`;
          table += `<td>${each['price']
            .toLocaleString('en-US', options)}</td>`;
          table += `<td>${each['maxTransaction']
            .toLocaleString('en-US', options)}</td>`;
          table += `<td>${each['direction']}</td>`;
          table += `</tr>`;
          idx++;
        }
  
        table += `
          </tbody>
        </table>
        `;
  
        $('#table-container').append(table);
        $('#spinner-loader').remove();
      },
    });
  });
  