<template>
  <div class="app-container">
    <div class="filter-container">
      <!-- <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" /> -->
      <!-- <el-select v-model="listQuery.importance" placeholder="Imp" clearable style="width: 90px" class="filter-item">
        <el-option v-for="item in importanceOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.type" placeholder="Type" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select> -->
      <!-- <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button> -->
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        新增人员
      </el-button>
      <!-- <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        导出信息
      </el-button> -->
      <!-- <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        reviewer
      </el-checkbox> -->
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
      >
      <el-table-column label="姓名" prop="username" sortable="custom" fixed="left" align="center" width="150" :class-name="getSortClass('id')">
        <template slot-scope="scope">
          <span>{{ scope.row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="性别" width="80px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.sex }}</span>
        </template>
      </el-table-column>
      <el-table-column label="病人情况" width="200px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.status }}</span>
        </template>
      </el-table-column>
      <el-table-column label="住院科室" width="200px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.keshi }}</span>
        </template>
      </el-table-column>
      <!-- <el-table-column label="病史" width="200px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.history }}</span>
        </template>
      </el-table-column> -->
      <el-table-column label="医生" width="180px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.doctor }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="200px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.id | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Status" class-name="status-col" width="100">
        <template slot-scope="{row}">
          <el-tag :type="row.status">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Actions" align="center" min-width="180px" fixed="right" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleShow(row)">
            查看
          </el-button>
          <el-button v-if="row.status!='published'" size="mini" type="success" @click="handleModifyStatus(row, 'edit')">
            编辑
          </el-button>
          <!-- <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDel(row)">
            删除
          </el-button> -->
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="姓名" prop="username">
          <el-input :disabled="formDisabled" v-model="temp.username" />
        </el-form-item>
        <el-form-item label="住院科室" prop="keshi">
          <el-select :disabled="formDisabled" v-model="temp.keshi" class="filter-item" placeholder="请选择">
            <el-option-group
              v-for="group in keshiOptions"
              :key="group.label"
              :label="group.label">
              <el-option
                v-for="item in group.options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-option-group>
          </el-select>
        </el-form-item>
        <el-form-item label="住院日期" prop="date">
          <el-date-picker :disabled="formDisabled" v-model="temp.date" type="datetime" placeholder="请选择日期" />
        </el-form-item>
        <el-form-item label="性别" prop="sex">
          <el-radio-group :disabled="formDisabled" v-model="temp.sex">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="病人情况">
          <el-select :disabled="formDisabled" v-model="temp.status" class="filter-item" placeholder="请选择">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input :disabled="formDisabled" v-model="temp.phone" />
        </el-form-item>
        <el-form-item label="所属医生" prop="doctor">
          <el-input :disabled="formDisabled" v-model="temp.doctor" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input :disabled="formDisabled" v-model="temp.email" />
        </el-form-item>
        <el-form-item label="身份证" prop="identity">
          <el-input :disabled="formDisabled" v-model="temp.identity" />
        </el-form-item>
        <el-form-item label="家庭地址">
          <el-row>
            <el-col :span="8">
              <el-select :disabled="formDisabled" v-model="temp.area1" placeholder="省">
                <!-- <el-option label="区域一" value="shanghai1"></el-option> -->
                <el-option value="河南省" selected="">河南省</el-option>
                <el-option value="江西省">江西省</el-option>
                <el-option value="福建省">福建省</el-option>
              </el-select>
            </el-col>
            <el-col :span="8">
              <el-select :disabled="formDisabled" v-model="temp.area2" placeholder="市">
                <!-- <el-el-option label="区域一" value="shanghai2"></el-el-option> -->
                <el-option value="许昌">许昌</el-option>
                <el-option value="郑州">郑州</el-option>
                <el-option value="漯河">漯河</el-option>
                <el-option value="南阳">南阳</el-option>
                <el-option value="信阳">信阳</el-option>
              </el-select>
            </el-col>
            <el-col :span="8">
              <el-select :disabled="formDisabled" v-model="temp.area3" placeholder="县/区">
                <!-- <el-el-option label="区域一" value="shanghai3"></el-el-option> -->
                <el-option value="舞阳县">舞阳县</el-option>
                <el-option value="源汇区">源汇区</el-option>
                <el-option value="临颍县">临颍县</el-option>
              </el-select>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="既往病史" prop="history">
          <el-input :disabled="formDisabled" type="textarea" v-model="temp.history" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button v-if="!formDisabled" type="primary" @click="createData">
          确认
        </el-button>
      </div>
    </el-dialog>

    <!-- <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog> -->
  </div>
</template>

<script>
import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import { getDoctorList, postDoctor } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})
const keshiOptions =  [{
  label: '内科',
  options: [{
    value: '呼吸内科',
    label: '呼吸内科'
  }, {
    value: '血液内科',
    label: '血液内科'
  },  {
    value: '消化内科',
    label: '消化内科'
  },  {
    value: '神经内科',
    label: '神经内科'
  }, {
    value: '肾脏内科',
    label: '肾脏内科'
  }, {
    value: '肿瘤内科',
    label: '肿瘤内科'
  }]
  }, {
  label: '外科',
  options: [{
    value: '普通外科',
    label: '普通外科'
  }, {
    value: '血管外科',
    label: '血管外科'
  }, {
    value: '胸外科',
    label: '胸外科'
  }, {
    value: '泌尿外科',
    label: '泌尿外科'
  }]
  }, {
  label: '其他科室',
  options: [{
    value: '放射科',
    label: '放射科'
  }, {
    value: '骨科',
    label: '骨科'
  }, {
    value: 'ICU',
    label: 'ICU'
  }, {
    value: '耳鼻喉科',
    label: '耳鼻喉科'
  }]
}]
export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      formDisabled: false,
      keshiOptions,
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        type: undefined,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['良好', '待确认', '待手术', '待观察', '危急'],
      showReviewer: false,
      temp: {
        id: +new Date(),
        username: '',
        keshi: '',
        date: '',
        sex: '男',
        phone: '',
        email: '',
        identity: '',
        doctor: '',
        area1: '',
        area2: '',
        area3: '',
        history: '',
        status: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '信息编辑',
        create: '信息录入'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getDoctorList().then(res => {
        console.log(res)
        this.list = res.list
        this.total = res.count

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleShow(row) {
      this.temp = row
      this.formDisabled = true
      this.dialogFormVisible = true
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    //
    handleModifyStatus(row, status) {
      this.resetTemp()
      this.formDisabled = false
      this.temp = row
      this.dialogFormVisible = true
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: +new Date(),
        username: '',
        keshi: '',
        date: '',
        sex: '男',
        phone: '',
        email: '',
        identity: '',
        doctor: '',
        area1: '',
        area2: '',
        area3: '',
        history: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.formDisabled = false
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      postDoctor(this.temp).then(() => {
        this.dialogFormVisible = false
        this.dialogStatus = ''
        this.getList()
        this.$notify({
          title: 'Success',
          message: '操作成功',
          type: 'success',
          duration: 1000
        })
      })
      // this.$refs['dataForm'].validate((valid) => {
      //   if (valid) {
      //     this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
      //     // this.temp.author = 'vue-element-admin'
      //     createArticle(this.temp).then(() => {
      //       this.list.unshift(this.temp)
      //       this.dialogFormVisible = false
      //       this.$notify({
      //         title: 'Success',
      //         message: 'Created Successfully',
      //         type: 'success',
      //         duration: 2000
      //       })
      //     })
      //   }
      // })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
            for (const v of this.list) {
              if (v.id === this.temp.id) {
                const index = this.list.indexOf(v)
                this.list.splice(index, 1, this.temp)
                break
              }
            }
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row) {
      this.$notify({
        title: 'Success',
        message: 'Delete Successfully',
        type: 'success',
        duration: 2000
      })
      const index = this.list.indexOf(row)
      this.list.splice(index, 1)
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal, this.list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}`
        ? 'ascending'
        : sort === `-${key}`
          ? 'descending'
          : ''
    }
  }
}
</script>

<style>
  .el-dialog {
    margin-bottom: 15vh;
  }
</style>
