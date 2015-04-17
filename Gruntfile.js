module.exports = function(grunt) {

  grunt.initConfig({
    // Comprimir js
    uglify: {
      js: {
        files: {
          'src/static/scripts/min.js': ['src/static/scripts/controllers/*.js']
        }
      } //my_target
    }, //uglify

    // Comprimir imagenes
    imagemin: {
/*NO funciona
      main: {

        files: [{
          expand: true,
          cwd: 'src/static/images/',
          src: ['*.{png,jpg,gif,.svg}'],
          dest: 'src/static/images/min/'
        }]

      }

    },//imagemin*/
    
    // Optimizador de las imagenes
    watch: {
      images: {

        files: ['src/static/images/*.{png,jpg,gif}'],
        tasks: ['newer:imagemin'],
        options: {
          spawn: false,
        }

      }//images
    }// watch

  });
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-newer');
  grunt.loadNpmTasks('grunt-contrib-imagemin');
  grunt.loadNpmTasks('grunt-contrib-watch');

};