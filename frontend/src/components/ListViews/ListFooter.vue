<!-- //// Neoffice — added file (no upstream equivalent) -->
<!-- //// The footer of every list: frappe-ui's own `ListFooter` writes « Load More » and « of » in English, in its template, where
     no catalogue reaches (« 4 of 4 » on a French desk). The `right` slot it offers is drawn here with translated text; the
     page-length buttons and the events stay frappe-ui's. To drop when frappe-ui translates its footer. -->
<template>
  <FrappeListFooter
    v-model="pageLengthCount"
    :options="options"
    @loadMore="emit('loadMore')"
  >
    <template #right>
      <div class="flex items-center">
        <Button
          v-if="showLoadMore"
          :label="__('Load More')"
          @click="emit('loadMore')"
        />
        <div v-if="showLoadMore" class="mx-3 h-[80%] border-l" />
        <div class="flex items-center gap-1 text-base text-ink-gray-5">
          {{
            __('{0} of {1}', [
              options.rowCount || '0',
              options.totalCount || '0',
            ])
          }}
        </div>
      </div>
    </template>
  </FrappeListFooter>
</template>

<script setup>
import { computed } from 'vue'
import { Button } from 'frappe-ui'
import { ListFooter as FrappeListFooter } from 'frappe-ui/experimental'

const props = defineProps({
  modelValue: { type: Number, default: 20 },
  options: {
    type: Object,
    default: () => ({
      rowCount: 0,
      totalCount: 0,
      pageLengthOptions: [20, 50, 100],
    }),
  },
})
const emit = defineEmits(['update:modelValue', 'loadMore'])

const pageLengthCount = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

// The same condition as frappe-ui's footer: a « Load More » only while some rows are still to come.
const showLoadMore = computed(
  () =>
    props.options.rowCount &&
    props.options.totalCount &&
    props.options.rowCount < props.options.totalCount,
)
</script>
