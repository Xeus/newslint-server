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
        },
        autoprefixer: {
            options: {
                browsers: ['last 3 version']
            },
            no_dest: {
                src: 'static/build/css/main.css'
            }
        },
        cssmin: {
            minify: {
                expand: true,
                cwd: 'static/build/css/',
                src: ['*.css', '!*.min.css'],
                dest: 'static/build/css/',
                ext: '.min.css'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-contrib-cssmin');

    grunt.registerTask('default', ['uglify', 'compass', 'autoprefixer', 'cssmin']);

};

