gems = {}


var variable = 1//theme program for gems.js
gems.theme = {
    vars: {
        using : 'default',
        themes : [
            {name: 'default', class: 'bg-light'},
            {name: 'dark', class: 'bg-dark'}
        ]
        
    },
    next: function() {
        for (var i = 0; i < this.vars.themes.length; i++) {
            if (this.vars.using == this.vars.themes[i].name) {
                this.vars.using = this.vars.themes[i + 1].name;
                document.body.className = this.vars.themes[i + 1].class;
                return;
            }
        }
    }
}

//add class into gems object
gems.magic = function() {
    gems.theme.next();
}