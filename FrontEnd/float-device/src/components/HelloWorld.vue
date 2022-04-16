<template>
  <div>
    <el-row>
      <button @click="back()">《</button>
    </el-row>
    <el-row :gutter="20" class="el-row" type="flex" justify="start" >
      <el-col v-for="dir in dirs" :key="dir" @click="dir_click(dir)">
          <el-button @click="dir_click(dir)">
            {{dir}}
          </el-button>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="el-row" type="flex" justify="start" >
      <el-col v-for="file in files" :key="file">
        <el-card> 
          {{file}}
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data:function(){
    return {
      cur_path:"/",
      files:[],
      dirs:[]
    }
  },
  
  methods:{
    _load_dir_and_file:function(data){
    if(data.code==200){
      data=JSON.parse(data.data);
      console.log({data});
      this.files=data.files;
      console.log(data.cur_path);
      this.cur_path=data.cur_path;
      console.log(this.cur_path);
      this.dirs=data.dirs;
      }
    },
    dir_click:function(dir){
      this.$axios
        .get('http://0.0.0.0:8888/?path='+this.cur_path+'/'+dir)
        .then(response =>{
          var data=response.data;
          this._load_dir_and_file(data);
        });
    },
    back:function(){
      this.$axios
        .get('http://0.0.0.0:8888/back?path='+this.cur_path)
        .then(response =>{
          var data=response.data;
          this._load_dir_and_file(data);
        });
    }
  },
  mounted () {
    this.$axios
      .get('http://0.0.0.0:8888')
      .then(response =>{
        var data=response.data;
        this._load_dir_and_file(data);
      });
  },
  
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
