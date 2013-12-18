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
        copy: {
            momentjs: {
                src: 'components/bower_components/momentjs/min/moment.min.js',
                dest: 'static/build/js/moment.min.js'
            },
            font_awesome: {
                src: 'components/bower_components/font-awesome/css/font-awesome.min.css',
                dest: 'static/build/css/font-awesome.min.css'
            },
            font_awesome_fonts: {
                cwd: 'components/bower_components/font-awesome/fonts/',
                src: '*',
                expand: true,
                dest: 'static/build/fonts/'
            },
            jquery: {
                src: 'components/bower_components/jquery/jquery.min.js',
                dest: 'static/build/js/jquery.min.js'
            },
            jquery_map: {
                src: 'components/bower_components/jquery/jquery.min.map',
                dest: 'static/build/js/jquery.min.map'
            },
            modernizr: {
                src: 'components/bower_components/modernizr/modernizr.min.js',
                dest: 'static/build/js/modernizr.min.js'
            }
        },
        compass: {
            dist: {
                options: {
                    sassDir: 'static/src/sass',
                    cssDir: 'static/build/css',
                    environment: 'production'
                }
            }
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
    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('build', ['uglify', 'copy', 'compass', 'autoprefixer', 'cssmin']);

};

