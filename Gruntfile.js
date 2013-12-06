module.exports = function(grunt) {
    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            all: {
                files: {
                    'static/build/js/<%= pkg.name %>.min.js': ['static/src/js/<%= pkg.name %>.js']
                }
            },
            modernizr: {
                files: {
                    'components/bower_components/modernizr/modernizr.min.js': ['components/bower_components/modernizr/modernizr.js']
                }
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

    grunt.registerTask('build', ['uglify', 'compass', 'autoprefixer', 'cssmin']);

};

