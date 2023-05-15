import onnx
from onnx import helper, TensorProto, numpy_helper

# 創建模型
model = helper.make_model(
    # 輸入張量，設定輸入形狀為(1, 1, 44100, 1)
    # (batch_size, channels, samples, features)
    inputs=[helper.make_tensor_value_info('input', TensorProto.FLOAT, (1, 1, 44100, 1))],

    # 輸出張量，設定輸出形狀為(1, 1)
    outputs=[helper.make_tensor_value_info('output', TensorProto.FLOAT, (1, 1))],

    # 創建計算圖
    nodes=[
        helper.make_node('Conv', ['input', 'weight'], ['conv_out'], kernel_shape=[3, 3], pads=[1, 1, 1, 1]),
        helper.make_node('Relu', ['conv_out'], ['relu_out']),
        helper.make_node('GlobalAveragePool', ['relu_out'], ['pool_out']),
        helper.make_node('Flatten', ['pool_out'], ['flatten_out']),
        helper.make_node('Gemm', ['flatten_out', 'weight2', 'bias'], ['gemm_out'], alpha=0.1, beta=0.2),
        helper.make_node('Sigmoid', ['gemm_out'], ['output'])
    ],

    # 設定模型的初始化權重
    initializer=[
        numpy_helper.from_array(np.random.randn(3, 3, 1, 32).astype(np.float32), name='weight'),
        numpy_helper.from_array(np.random.randn(32, 1).astype(np.float32), name='bias'),
        numpy_helper.from_array(np.random.randn(288, 64).astype(np.float32), name='weight2')
    ],

    # 設定模型的圖形輸出名稱
    output_names=['output']
)

onnx.save(model, 'model.onnx')

