<template>
  <div id="check">
    <el-card>
      <div id="search">
        <el-input v-model="search" placeholder="按类别搜索" style="width: 300px" @input="pageList" />
      </div>
      <div id="actionButton" style="margin-left:73%;margin-bottom: 20px;margin-top: -40px">
        <el-button type="primary" :disabled="disabled.verify" @click="verifyTest">预检验</el-button>
        <el-button type="primary" :disabled="disabled.verify" @click="verifyCase">检验</el-button>
        <el-button type="primary" :disabled="disabled.reset" @click="resetCase">重置</el-button>
      </div>
      <div id="table">
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          @selection-change="handleSelection"
          @filter-change="handleFilterChange"
          v-loading="loading"
          element-loading-text="正在验证，请耐心等候..."
        >
          <el-table-column type="selection" width="40px" align="center"> </el-table-column>
          <el-table-column prop="id" label="序号" width="80" align="center"> </el-table-column>
          <el-table-column prop="element" label="类别" width="100" :filters="filterData" column-key="element" align="center"> </el-table-column>
          <el-table-column prop="rule_describe" label="规则描述" align="center" width="100"> </el-table-column>
          <el-table-column prop="name" label="名称" align="center" width="100"> </el-table-column>
          <el-table-column prop="describe" label="描述" align="center" width="100"> </el-table-column>
          <el-table-column prop="content" label="规格化描述" align="center"> </el-table-column>
          <el-table-column prop="result" label="验证结果" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.result === '符合' ? 'primary' : 'success'" disable-transitions>{{ scope.row.result }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="last_result" label="上一次验证结果" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.last_result === '符合' ? 'primary' : 'success'" disable-transitions>{{ scope.row.last_result }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="count" label="验证次数" width="80" align="center"> </el-table-column>
        </el-table>
      </div>
      <div id="page">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[1, 2, 5, 7, 10]"
          :page-size="pagination.limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          style="margin-left: 30%;margin-top: 20px"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Check.vue',
  data() {
    return {
      tableData: [],
      loading: false,
      filterData: [
        { text: '外部接口', value: '外部接口' },
        { text: '功能处理', value: '功能处理' },
        { text: '功能层次', value: '功能层次' },
        { text: '状态迁移', value: '状态迁移' },
        { text: '其他', value: '其他' }
      ],
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      search: '', //搜索框
      visible: {
        addDialog: false,
        deleteDialog: false,
        editDialog: false
      },
      disabled: {
        reset: true,
        verify: true
      },
      editForm: {
        //修改时使用
        name: '',
        type: '',
        describe: '',
        remark: ''
      },
      addForm: {
        //添加使用
        name: '',
        type: '',
        describe: '',
        remark: ''
      },
      resetData: [],
      verifyData: [],
      left_rules: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        remark: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      options: [
        {
          value: '外部接口',
          label: '外部接口'
        },
        {
          value: '功能处理',
          label: '功能处理'
        },
        {
          value: '功能层次',
          label: '功能层次'
        },
        {
          value: '状态迁移',
          label: '状态迁移'
        },
        {
          value: '其他',
          label: '其他'
        }
      ],
      itemInfo: '',
      caseInfo: ''
    }
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .post(this.Global_Api + '/api/case_list', this.itemInfo.id)
        .then(response => {
          this.data = response.data.case_list
          this.left_rules = response.data.left_rules_id
          this.caseInfo = response.data.info
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    getList() {
      // 处理数据，根据表格中name字段来筛选
      let list = this.data.filter((item, index) => item.element.includes(this.search))
      // let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
      if (this.caseInfo !== '') {
        alert(this.caseInfo)
      } else if (this.left_rules.length !== 0) {
        alert('此项目中以下规则未实例化：\nid: ' + this.left_rules)
      }
    },
    handleFilterChange(value) {
      console.log(value)
      if (value['element']) {
        this.filterSearch = value['element']
        let list = this.data.filter((item, index) => item.element.includes(this.filterSearch))
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
      if (value['type']) {
        this.filterSearch = value['type']
        let list = this.data.filter((item, index) => item.type.includes(this.filterSearch))
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
    },
    handleSizeChange(val) {
      // 当每页数量改变
      console.log(`每页 ${val} 条`)
      this.pagination.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      // 当当前页改变
      console.log(`当前页: ${val}`)
      this.pagination.page = val
      this.getList()
    },
    handleSelection(val) {
      console.log(val)
      // 删除按钮
      if (val.length === 0) {
        this.disabled.reset = true
        this.disabled.verify = true
      } else {
        this.disabled.reset = false
        this.disabled.verify = false
        this.resetData = val
        this.verifyData = val
        console.log(val)
      }
    },
    verifyCase() {
      this.loading = true
      this.$http
        .post(this.Global_Api + '/api/verify_case', this.verifyData)
        .then(response => {
          if (response.data.error_code === 0) {
            this.loading = false
            this.pageList()
          } else {
            console.log(response.data)
            this.loading = false
            alert('error!!!!')
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    verifyTest() {
      this.loading = true
      this.$http
        .post(this.Global_Api + '/api/verify_case_test', this.verifyData)
        .then(response => {
          if (response.data.error_code === 0) {
            this.loading = false
            this.pageList()
          } else {
            console.log(response.data)
            this.loading = false
            alert('error!!!!')
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    resetCase() {
      this.loading = true
      this.$http
        .post(this.Global_Api + '/api/reset_case', this.resetData)
        .then(response => {
          if (response.data.error_code === 0) {
            this.loading = false
            this.pageList()
          } else {
            console.log(response.data)
            this.loading = false
            alert('error!!!!')
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('ss', this.itemInfo)
    }
  }
}
</script>

<style scoped></style>
