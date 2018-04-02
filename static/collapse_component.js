
class TryClass {
  constructor(name) {
    this.name = name;
  }

  sayHi() {
    alert( this.name );
  }

  getName() {
    return this.name;
  }
}

class CollapseComponent {
  constructor( d3_item )
  {
    this.d3_item = d3_item;
  }

  plot_me() {
    var data = [75, 10, 15, 20, 25]

    var dataset = [];
    for( var i=0 ; i<25 ; i++ ) {
      var newNumber = Math.random() * 30;
      dataset.push( newNumber );
    }

    // d3.select( "body").append( "p").text( "New Para!@@" );

    // d3.select( "body" ).selectAll( "p")
    //   .data( data )
    //   .enter()
    //   .append("p")
    //   .text(
    //     function(d) {
    //       return d*d;
    //     }
    //    );

    this.d3_item.data( dataset )
      .enter()
      .append( "div" )
      .attr( "class", "bar" )
      .style(
        "height",
        function(d) {
          return d*5+"px";
        })
      .style(
        "margin-right",
        function(d) {
          return "1px";
        }
      )
      ;
  }

}
