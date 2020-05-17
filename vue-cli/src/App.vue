<template>
    <div class="container">
        <div class="row">
            <div class="col-xs-12">
                <transition
                    enter-active-class="animated zoomIn"

                >
                <router-view></router-view>
                </transition>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
       
    }
</script>

<style>
 
</style>
