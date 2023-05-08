// Vista
class Articulos extends React.Component {
    constructor(props) {
      super(props);
      this.state = { articulos: [], error: null };
    }
  
    componentDidMount() {
      Controlador.obtenerArticulos(this.props.revista)
        .then(articulos => this.setState({ articulos }))
        .catch(error => this.setState({ error }));
    }
  
    render() {
      if (this.state.error) {
        return <ErrorMessage message={this.state.error.message} />;
      }
      return (
        <div>
          {this.state.articulos.map(articulo => (
            <Articulo key={articulo.doi} {...articulo} />
          ))}
        </div>
      );
    }
}