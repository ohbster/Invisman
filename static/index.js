new gridjs.Grid({
//const grid = new Grid({
  columns: [
    { id: "id", name: "Id" },
    { id: "name", name: "Name" },
    { id: "image", name: "Image" },
    //{ id: "description", name: "Description" },
    { id: "msrp", name: "MSRP" },
  ],
  server: {
    url: 'http://127.0.0.1:5000/api/products',
    then: results => results.data
  }
// });
}).render(document.getElementById("wrapper"));
  // data: [
  //   ["John", "john@example.com", "(353) 01 222 3333"],
  //   ["Mark", "mark@gmail.com", "(01) 22 888 4444"],
  //   ["Eoin", "eoin@gmail.com", "0097 22 654 00033"],
  //   ["Sarah", "sarahcdd@gmail.com", "+322 876 1233"],
  //   ["Afshin", "afshin@mail.com", "(353) 22 87 8356"]
  // ]

// }).render(document.getElementById("wrapper"));
