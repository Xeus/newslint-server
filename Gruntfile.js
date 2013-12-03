module.exports = function(grunt) {
    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
            },
            build: {
                src: 'static/src/js/<%= pkg.name %>.js',
                dest: 'static/build/js/<%= pkg.name %>.min.js'
            }
        },
        compass: {
            dist: {
                options: {
                    sassDir: 'static/src/sass',
                    cssDir: 'static/build/css',
                    environment: 'production'
                }
            },
            // dev: {
            //     options: {
            //         sassDir: 'sass',
            //         cssDir: 'css'
            //     }
            // }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-jshint');

    grunt.registerTask('default', ['uglify', 'compass']);

};

