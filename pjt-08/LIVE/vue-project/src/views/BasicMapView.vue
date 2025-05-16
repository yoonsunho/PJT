<template>
  <!-- 사용자의 입력 받기 -->
  <input v-model="keyword" @input="updateMap"/> <br>    
  <iframe :src="mapUrl"></iframe>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const lat = ref(null)
const lng = ref(null)
const mapUrl = ref('')
const keyword = ref('')

// 위치 정보 가져오기
const getCurrentLocation = () => {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      lat.value = pos.coords.latitude   // 위도 경도 가녀오기
      lng.value = pos.coords.longitude
      updateMap() // 위치 받자마자 최초 1회 지도 표시
    },
  )
}

// iframe 지도 업데이트
const updateMap = () => {
  mapUrl.value =
    `https://maps.google.com/maps` +
    `?ll=${lat.value},${lng.value}` +
    `&z=14` +
    `&output=embed` 
    + `&q=${keyword.value.trim()}`    // v-model로 양방향 바인딘 된 키웓드 값을 입력 이반트 발생할 때 마다 updateMap호출해서 
                                      
}

// 초기 위치 설정
onMounted(() => { //마운트 된 순간 실행
  getCurrentLocation()
})

</script>
