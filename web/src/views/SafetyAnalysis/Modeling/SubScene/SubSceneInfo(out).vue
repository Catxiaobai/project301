<template>
  <div id="subSceneInfo">
    <div class="divHelp">
      <el-popover placement="bottom" title="help" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <p>此页面可以对使用场景进行增删改查操作</p>
        <el-button icon="el-icon-message-solid" circle slot="reference"></el-button>
      </el-popover>
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <div>
          <p>此页面可以对使用场景进行增删改查操作</p>
        </div>
        <el-button type="text" slot="reference">操作提示</el-button>
      </el-popover>
    </div>
    <!--    标题-->
    <!--    <span>项目名称</span>-->
    <el-card class="tableTitle">
      <span style="font-size: large;margin-left: 10px;margin-right: 10px">选择模型类型</span>
      <el-select v-model="value" placeholder="请选择" @change="onChange">
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
      </el-select>
      <el-button size="20px" type="success" style="margin-left: 580px" @click="handleAdd" icon="el-icon-plus">添加新场景</el-button>
      <!--    </el-card>-->
      <!--    &lt;!&ndash;    表格内容&ndash;&gt;-->
      <!--    <el-card class="traceTable" style="margin-top: 20px">-->
      <el-table :data="tableData" style="width: 100%;margin-top: 40px" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
        <el-table-column label="序号" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.trace_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="名称" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.trace_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="类型" width="180px" align="center">
          <template>
            <span style="margin-left: 10px">状态机</span>
          </template>
        </el-table-column>
        <el-table-column label="场景介绍" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.trace_describe }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>
            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--    </el-card>-->
      <!--    &lt;!&ndash;    分页显示&ndash;&gt;-->
      <!--    <el-card class="tablePage" style="margin-top: 20px">-->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[1, 2, 5, 7, 10]"
        :page-size="limit"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-left: 30%;margin-top: 30px"
      >
      </el-pagination>
    </el-card>
    <!--    查看trace弹窗-->
    <!--    todo: 展示效果不好-->
    <el-dialog title="查看场景" :visible.sync="dialogShowTrace">
      <span style="display: block">场景名称：{{ showTrace.trace_name }}</span>
      <span style="margin-top: 10px;display: block">场景内容：</span>
      <span style="display: block;white-space: pre-line">{{ showTrace.trace_content }}</span>
      <span style="margin-top: 10px;display: block;white-space: pre-line">场景详情：{{ showTrace.trace_details }}</span>
      <span slot="footer" class="dialog-footer">
        <!--        <el-button @click="dialogShowTrace = false">取 消</el-button>-->
        <el-button type="primary" @click="dialogShowTrace = false">OK</el-button>
      </span>
    </el-dialog>
    <!--    添加场景弹窗-->
    <el-dialog title="添加场景" :visible.sync="dialogAddTrace">
      <el-form :model="addForm" :rules="rules" ref="addForm">
        <el-form-item label="场景名称" label-width="120px" prop="name">
          <el-input v-model="addForm.name" clearable placeholder="请输入场景名称"></el-input>
        </el-form-item>
        <el-form-item label="场景内容" label-width="120px" prop="content">
          <el-input v-model="addForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景具体内容"> </el-input>
        </el-form-item>
        <el-form-item label="场景描述" label-width="120px" prop="details">
          <el-input v-model="addForm.details" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景文字描述"> </el-input>
        </el-form-item>
        <el-form-item label="场景介绍" label-width="120px" prop="describe">
          <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景简单介绍"> </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddTrace = false">取 消</el-button>
        <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
      </div>
    </el-dialog>
    <!--    编辑场景弹窗-->
    <el-dialog title="编辑此场景" :visible.sync="dialogEditTrace">
      <el-form :model="editForm" :rules="rules" ref="editForm">
        <el-form-item label="场景名称" label-width="120px" prop="name">
          <el-input v-model="editForm.name" clearable placeholder="请输入场景名称"></el-input>
        </el-form-item>
        <el-form-item label="场景内容" label-width="120px" prop="content">
          <el-input v-model="editForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景具体内容"> </el-input>
        </el-form-item>
        <el-form-item label="场景描述" label-width="120px" prop="details">
          <el-input v-model="editForm.details" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景文字描述"> </el-input>
        </el-form-item>
        <el-form-item label="场景介绍" label-width="120px" prop="describe">
          <el-input v-model="editForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景简单介绍"> </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogEditTrace = false">取 消</el-button>
        <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'SubSceneInfo.vue',
  data() {
    return {
      limit: 7, //每页显示条数
      total: null, //trace总数
      page: 1, //第几页
      search: '', //搜索框
      dialogShowTrace: false, //查看trace弹窗
      dialogAddTrace: false, //添加trace弹窗
      dialogEditTrace: false, //编辑trace
      tableData: [], //trace表
      showTrace: {}, //查看trace
      addForm: {
        //添加时使用
        name: '',
        content: '',
        details: '',
        describe: ''
      },
      editForm: {
        //编辑trace
        id: '',
        name: '',
        content: '',
        details: '',
        describe: ''
      },
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        content: [{ required: true, message: '不能为空', trigger: 'blur' }],
        details: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      options: [
        {
          value: '状态机',
          label: '状态机'
        },
        {
          value: '时序图',
          label: '时序图'
        },
        {
          value: '用例图',
          label: '用例图'
        },
        {
          value: '活动图',
          label: '活动图'
        }
      ],
      value: '状态机'
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get(this.Global_Api + '/api/trace_list')
        .then(response => {
          // console.log(response.data.trace_list)
          this.data = response.data.trace_list
          this.data2 = response.data.trace_list
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    // 处理数据
    getList() {
      // es6过滤得到满足搜索条件的展示数据list
      // eslint-disable-next-line no-unused-vars
      // console.log({ test: this.search })
      let list = this.data.filter((item, index) => item.trace_describe.includes(this.search))
      // let list = this.data
      this.tableData = list.filter((item, index) => index < this.page * this.limit && index >= this.limit * (this.page - 1))
      this.total = list.length
    },
    // 当每页数量改变
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.limit = val
      this.getList()
    },
    // 当当前页改变
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.page = val
      this.getList()
    },
    handleShow(index, row) {
      this.dialogShowTrace = true
      // console.log(index, row)
      this.showTrace = row
    },
    handleEdit(index, row) {
      // console.log(index, row)
      this.editForm.id = row.trace_id
      this.editForm.name = row.trace_name
      this.editForm.content = row.trace_content
      this.editForm.describe = row.trace_describe
      this.editForm.details = row.trace_details
      this.dialogEditTrace = true
    },
    handleDelete(index, row) {
      // console.log(index, row)
      this.$confirm('此操作将删除该trace, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          console.log(row.trace_id)
          this.$http
            .post(this.Global_Api + '/api/delete_trace', { trace_id: row.trace_id })
            .then(response => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                })
                this.pageList()
              }
            })
            .catch(function(error) {
              console.log(error)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    handleAdd() {
      this.dialogAddTrace = true
    },
    handleAddCommit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // alert('submit!')
          this.dialogAddTrace = false
          console.log(this.addForm)
          this.$http
            .post(this.Global_Api + '/api/add_trace', this.addForm)
            .then(response => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.pageList()
              }
            })
            .catch(function(error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleEditCommit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // alert('submit!');
          this.dialogEditTrace = false
          console.log(this.addForm)
          this.$http
            .post(this.Global_Api + '/api/edit_trace', this.editForm)
            .then(response => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.pageList()
              }
            })
            .catch(function(error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    filterTag(value, row) {
      return row.type === value
    },
    onChange(value) {
      console.log(value)
      if (value != '状态机') {
        this.data = []
      } else {
        this.data = this.data2
      }
      this.getList()
    }
  },
  mounted() {
    //   this.$notify({
    //     title: '提示',
    //     message: '此页面可以实现对使用场景的增删改查操作',
    //     duration: 0,
    //     offset: 200
    //   })
  }
}
</script>

<style lang="scss" scoped>
.divHelp {
  margin-left: 1100px;
  height: 40px;
  margin-top: -40px;
}
</style>
